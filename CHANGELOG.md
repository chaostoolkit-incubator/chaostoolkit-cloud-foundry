# Changelog

## [Unreleased][]

[Unreleased]: https://github.com/chaostoolkit/chaostoolkit-cloud-foundry/compare/0.7.2...HEAD

## [0.7.2][]

[0.7.2]: https://github.com/chaostoolkit/chaostoolkit-cloud-foundry/compare/0.7.1...0.7.2

### Changed

 - Modernize to use github action
 - Fixed python minimal version pattern
 - Requires now Python 3.7 as other packages

## [0.7.1][]

[0.7.1]: https://github.com/chaostoolkit/chaostoolkit-cloud-foundry/compare/0.7.0...0.7.1

### Changed

 - Fixed "get_bind_by_name" to use the CF API specs

## [0.7.0][]

[0.7.0]: https://github.com/chaostoolkit/chaostoolkit-cloud-foundry/compare/0.6.0...0.7.0

### Added

 -   Add "Stop All CF applications for the specified org name" action
 -   Add "Start a CF application" action
 -   Add "Start All CF applications for the specified org name" action

## [0.6.0][]

[0.6.0]: https://github.com/chaostoolkit/chaostoolkit-cloud-foundry/compare/0.5.1...0.6.0

### Added

-   Add "Stop CF application" action

## [0.5.1][]

[0.5.1]: https://github.com/chaostoolkit/chaostoolkit-cloud-foundry/compare/0.5.0...0.5.1

### Changed

-   Read version from source code without importing when deps are not available yet

## [0.5.0][]

[0.5.0]: https://github.com/chaostoolkit/chaostoolkit-cloud-foundry/compare/0.4.0...0.5.0

### Changed

-   Add "Unbind from service" action
-   Add basic examples to un agains a live Cloud Foundry
-   Add "unmap and map route" actions

## [0.4.0][]

[0.4.0]: https://github.com/chaostoolkit/chaostoolkit-cloud-foundry/compare/0.3.1...0.4.0

### Changed

-   Do not discover system properties as it is not used by chaostoolkit anyway

## [0.3.1][]

[0.3.1]: https://github.com/chaostoolkit/chaostoolkit-cloud-foundry/compare/0.3.0...0.3.1

### Changed

-   expect token in secrets not in configuration

## [0.3.0][]

[0.3.0]: https://github.com/chaostoolkit/chaostoolkit-cloud-foundry/compare/0.2.1...0.3.0

### Added

-   discovery support [#4][4]

[4]: https://github.com/chaostoolkit-incubator/chaostoolkit-cloud-foundry/issues/4

## [0.2.1][]

[0.2.1]: https://github.com/chaostoolkit/chaostoolkit-cloud-foundry/compare/0.2.0...0.2.1

### Added

-   requirements-dev.txt to MANIFEST.in

## [0.2.0][]

[0.2.0]: https://github.com/chaostoolkit/chaostoolkit-cloud-foundry/compare/0.1.0...0.2.0

### Added

-   MANIFEST.in to package up non source code files

## [0.1.0][]

[0.1.0]: https://github.com/chaostoolkit/chaostoolkit-cloud-foundry/tree/0.1.0

### Added

-   Initial release