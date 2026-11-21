# Feature Hero Constitution

Feature Hero exists to facilitate the processing of tabular data and reduce the
manual work required to prepare variables and evaluate regression models.

Its objective is to provide a CLI that transforms datasets, automatically selects
variables through genetic algorithms, optimizes regression models, and exports
analyzable results.

## Core Principles

### I. Developer-Focused Tooling

Feature Hero MUST serve people with development and data-science knowledge. It is
not designed as an end-user application. Public behavior MUST remain explicit,
scriptable, and accessible through the CLI so that users can control inputs,
parameters, and outputs.

### II. Performance and Optimization

The application MUST prioritize high-performance execution for data preparation,
genetic optimization, and regression evaluation. Solutions MUST use the existing
optimization and regression capabilities when they satisfy the specification,
avoiding unnecessary processing and avoidable complexity.

### III. Functional and Measurable Objectives

Every feature MUST define clear objectives and verifiable behavior. Implementation
work MUST directly support the approved specification, with inputs, outputs,
validations, and failure conditions made explicit where applicable.

### IV. Specification Fidelity and Minimal Scope

Development MUST cover only what the specification requests. The project MUST
not add optional enhancements, speculative abstractions, or unrelated refactors.
Changes MUST be the smallest functional change that satisfies the specification.

### V. Critical Improvement and Delivery Efficiency

Improvements outside the specification MAY be made only when they are critical to
correctness, security, performance, or maintainability required for the specified
behavior. Work MUST remain focused on reaching the defined objective in the
shortest reasonable delivery path.

## Project Scope

The project covers tabular-data transformation, dataset validation, genetic
feature selection, regression-model optimization, background job management,
result analysis, and export of derived artifacts through the `featurehero` CLI.
The project does not include user-facing application interfaces or functionality
not required by an approved specification.

## Technical Constraints

- The implementation MUST remain compatible with Python `>=3.12,<4.0`.
- The public CLI command names and their documented parameters MUST remain stable
  unless a specification explicitly changes them.
- Supported data formats, transformations, metrics, and model options MUST be
  validated at the system boundary.
- Results MUST be exportable in the formats and locations defined by the
  specification.

## Development Workflow

- Work MUST begin from an approved specification and remain traceable to it.
- Each implementation MUST include the validation needed to demonstrate the
  specified behavior.
- Speckit actions MUST preserve the configured Git workflow, including feature
  creation and stage commits.
- A change MUST be reviewed for scope compliance before delivery; unrequested work
  MUST be removed or deferred.

## Governance

This constitution governs project decisions and supersedes informal practices when
they conflict. Amendments require an explicit request, an updated version, a
recorded rationale, and validation that the change does not weaken the principles.

Constitution versions use semantic versioning: MAJOR for incompatible principle
changes or removals, MINOR for new principles or materially expanded governance,
and PATCH for clarifications or non-semantic corrections. Every specification,
plan, task list, and implementation review MUST check compliance with this
constitution.

**Version**: 1.0.0 | **Ratified**: 2026-11-21 | **Last Amended**: 2026-11-21
