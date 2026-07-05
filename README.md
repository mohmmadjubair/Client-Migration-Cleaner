# Client Migration Cleaner

A command-line Python tool for cleaning and validating messy customer data
exports before importing them into a target system. Built to handle the
kinds of data quality issues that come up during practice management system
migrations.

## Why I built this

I'm preparing for a Customer Implementation Engineer role and wanted a
project that mirrored the actual work: taking messy customer exports,
cleaning what's safely cleanable, and flagging anything ambiguous for
human review.

The interesting part isn't the code, it's the design decisions about
where to auto-fix and where to flag. My core rule was "never silently
guess" — any ambiguous row goes to a review file with a reason attached,
so a human decides what to do.

## What it does

- Normalises whitespace and casing in name and suburb fields
- Lowercases email addresses and strips whitespace
- Standardises phone numbers to E.164 format using the `phonenumbers` library
- Validates rows against required-field and format rules
- Detects duplicate clients by email with row tracing back to the first occurrence
- Routes any row that can't be safely cleaned to a review CSV with a reason attached
- CLI so it can be pointed at any input/output paths

## Design principles

- **Never silently guess.** Every rejected row gets a reason attached, so a human can decide.
- **Separation of concerns.** Normalisation, validation, and I/O each live in their own module.
- **Return-a-reason pattern.** Validators return `(bool, reason)` tuples so problems are self-documenting downstream.

## Project structure
