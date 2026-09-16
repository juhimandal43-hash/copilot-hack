# Coding with an AI pair programmer

[GitHub Copilot](https://github.com/features/copilot) is your AI pair programmer, built to support you throughout your development experience. As with any new tool, using GitHub Copilot requires learning a few new skills. This project is built to do exactly that, to give you an opportunity to build a project, using the language and tools you typically use, with GitHub Copilot.

> **[Start hacking!](./hackathon.md)**

## Requirements

This project is configured with a [devcontainer](./.devcontainer/devcontainer.json), which can be [run locally](https://code.visualstudio.com/docs/devcontainers/containers) or in a [codespace](https://github.com/features/codespaces). Please refer to the [setup exercise](./content/0-get-started.md) for more information.

The project does assume you are familiar with programming, but is not prescriptive about language or framework choice.

## PulsePilot exercise app

This repository also includes a self-contained, standard-library Tkinter exercise helper. It collects age, weight, and height, shows a neutral BMI profile, suggests an adjustable starter routine with concrete push-up, squat, lunge, and plank sets/reps or durations, and includes a daily movement reminder plus visible device-local toast notifications for profile and checklist activity.

Run it from the repository root:

```sh
python exercise_app.py
```

Run the pure-logic tests:

```sh
python -m unittest discover -s tests -v
python -m py_compile exercise_app.py
```

Limitations: suggestions are general educational guidance, BMI is only a rough screening measure, and reminders/toasts run only while the app is open (they do not provide phone or background notifications). Consult a qualified clinician for personalized exercise advice; stop and seek medical help for alarming symptoms.

## License 

This project is licensed under the terms of the MIT open source license. Please refer to [MIT](./LICENSE.txt) for the full terms.

## Maintainers 

You can find the list of maintainers in [CODEOWNERS](./.github/CODEOWNERS)

## Support

This project is provided as-is, and may be updated over time. If you have questions, please [open an issue](/issues/new).
