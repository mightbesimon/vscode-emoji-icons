# How to Contribute

Thank you for either opening a pull request or an issue. I makes me feel like people like using my creations and care enough to give back! 😊

There are three ways you can contribute:

- emoji proposals
- raise issues
- architectural suggestions

For the best chance of your contribution making into the next release, please follow these steps for pull requests and issues respectively.

## Emoji Proposal Pull Requests

1. add your proposals in one of the existing `.md` reference files inside `reference/` folder
1. run build task (cmd+shift+B) or `$ python3 -m translate` to generate json theme files
1. start debug (F5) to preview your changes

> ⚠️ Do not commit any `*icon-theme.json` files, these will be generated in the CI/CD workflow

> ⚠️ For compatibility purposes, please try to use emojis release in 2019 or earlier. You may check your emojis [here](https://unicode.org/emoji/charts/emoji-versions.html)

In `references/*.md` files, each proposal has to follow the following format rules exactly.

- start the line with a `-`, all other lines are considered comments
- **one** emoji per line
- iconId can use the or operator ` | ` (one space each side)
- extensions should start with `.`
- anything in brackets after iconId are considered comments

examples:

yes

```markdown
- 😊 option1.md | option2.txt
- ❤️ .extension (optional comment)
```
no

```markdown
- 1️⃣2️⃣ filename (two emojis one line)
- 😔 leftNoSpace.ts|rightNoSpace.js
- 👎 (comment out of place) .extension
```

## Issues

Screenshots are much appriciated but not required.
