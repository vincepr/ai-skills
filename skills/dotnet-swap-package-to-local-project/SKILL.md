---
name: dotnet-swap-package-to-local-project
description: Temporarily replace a NuGet PackageReference with a local ProjectReference. Use when testing unpublished package source in a .NET repository.
---

# Swap a NuGet Package for a Local Project

Replace a NuGet `PackageReference` with a local `ProjectReference` for testing. Preserve the original package declarations as commented `TODO` lines so the swap is easy to revert.

## Never Commit the Swap

Treat the swap as local-only scaffolding. Its project path depends on the developer's local checkout and may break every other environment.

- Never stage, commit, push, or include the swap in a pull or merge request.
- Before committing other work, restore the package declarations and remove the temporary project reference.
- If the user explicitly asks to commit the swap, confirm that intent before proceeding.

## Prefer an Available Package

Before editing, check whether the desired package version is already available from a configured feed. A published preview or prerelease is more portable than a local project reference.

Use the published version when it represents the source the user wants to test. Use a local swap when no suitable package exists or when testing uncommitted local changes.

## Gather and Verify Inputs

Obtain:

1. The NuGet package ID, such as `Example.Component`.
2. The absolute path to the replacement `.csproj`, such as `/path/to/example-component/src/Example.Component/Example.Component.csproj`.
3. The consumer projects to modify when more than one project references the package.

Ask for missing values directly. Do not guess paths. Verify the replacement project exists.

Inspect the replacement repository before trusting its source:

```bash
git -C <replacement-repo-root> status --short
git -C <replacement-repo-root> branch --show-current
```

Confirm that its branch and working tree represent the source the user intends to test. Do not change branches or discard work without authorization.

## Perform the Swap

1. Locate direct consumers:

   ```bash
   rg -l '<PackageReference[^>]+Include="<PackageId>"' --glob '*.csproj'
   ```

   If multiple projects consume the package, ask which ones to change.

2. Determine where the version is declared:

   - With Central Package Management, find the matching `<PackageVersion>` in the applicable `Directory.Packages.props`.
   - Without Central Package Management, the version may be on the `PackageReference` itself.
   - If the dependency is only transitive and has no direct `PackageReference`, stop and ask which consumer should receive the local `ProjectReference`.

3. In each selected consumer project:

   - Comment out the original `PackageReference` without altering its contents.
   - Add a `TODO` explaining how to restore it.
   - Add a temporary `ProjectReference` using a relative path from that consumer project.
   - Place the reference in an existing project-reference `ItemGroup`, or create a focused `ItemGroup` when none exists.

4. When Central Package Management supplies the version, comment out the matching `PackageVersion` and add its revert `TODO`. Do not remove unrelated central versions.

5. Review the diff and build every affected consumer using the repository's normal build settings:

   ```bash
   dotnet build <consumer-project>
   ```

   If the build fails, report the failure. Do not silently revert or broaden the swap.

## Comment Format

In `Directory.Packages.props`:

```xml
<!-- TODO: restore PackageVersion after local testing of <PackageId> -->
<!-- <PackageVersion Include="<PackageId>" Version="<original-version>" /> -->
```

In the consumer project:

```xml
<!-- TODO: restore PackageReference after local testing of <PackageId> -->
<!-- <PackageReference Include="<PackageId>" /> -->

<!-- TODO: remove this local ProjectReference and restore the PackageReference after testing -->
<ProjectReference Include="<relative-path-to-replacement-project>" />
```

Preserve additional attributes from the original declarations inside the comments.

## Edge Cases

- If the local project introduces a conflicting transitive dependency, report the restore or build diagnostics. Do not swap additional packages without asking.
- Compute the relative path separately for each consumer project.
- Do not create a local feed or `nuget.config`; that is a different workflow.
- If generated or conditional MSBuild files control the reference, explain the indirection before editing it.

## Report

Tell the user:

- Which package and projects were swapped.
- Which files changed and which local project path was used.
- Whether the affected projects built successfully.
- How to revert the swap.
- That the local-only edits must be reverted before staging or committing.
