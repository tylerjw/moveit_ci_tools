# MoveIt CI Tools

This package contains tools to enable CI testing.

## colcon_list_packages_changed_since

Use this to list the ROS packages in a git repo that have changed since some point in the history.
This has the same output as `colcon list`.  It depends on `colcon` and `git` being installed.

### Use with ament_clang_tidy

[This PR](https://github.com/ament/ament_lint/pull/287) adds the `--packages_select` argument to ament_clang_tidy to enable you to use it with `colcon_list_packages_changed_since` for running clang-tidy over packages changed since some point.

The PR was merged but ament_lint has not yet been released with this new feature.  As a result you'll need a local build of ament_lint sourced.

This package can be used with ament_clang_tidy to run clang_tidy for only packages that have changed since some branch.  For example if you have a PR against the master branch of moveit you would do this to do an ament-tidy test over just the packages in moveit your change affects:

```bash
packages_with_changes=$(colcon_list_packages_changed_since --names-only src/moveit master)
ament_clang_tidy --config src/moveit/.clang-tidy --packages-select $packages_with_changes
```

Note that this command must be run from the root of the workspace and `compile_commands.json` files need to be generated durring a build of moveit.

To enable them with `colcon build` add this argument: `--mixin compile-commands`.

To enable them with `catkin configure` add this to your `--cmake-args`: `-DCMAKE_EXPORT_COMPILE_COMMANDS=ON`.
