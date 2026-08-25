# GitHub Profile README Setup

## 1. Repository

Create a public repository named exactly:

`Anagh-007`

GitHub automatically uses `README.md` from this repository as your profile README.

## 2. Files

Keep this structure:

```text
Anagh-007/
├── README.md
├── SETUP.md
├── assets/
│   ├── profile.jpg
│   ├── portrait.svg
│   ├── radar-dark.svg
│   ├── radar-light.svg
│   ├── radar-langs-dark.svg
│   ├── radar-langs-light.svg
│   ├── card-crowdx-dark.svg
│   ├── card-crowdx-light.svg
│   ├── card-ai-assistant-dark.svg
│   ├── card-ai-assistant-light.svg
│   ├── card-athlete-fit-dark.svg
│   ├── card-athlete-fit-light.svg
│   ├── card-face-detection-dark.svg
│   └── card-face-detection-light.svg
└── .github/
    └── workflows/
        └── snake.yml
```

## 3. Push the files

```bash
git init
git add .
git commit -m "Create GitHub profile README"
git branch -M main
git remote add origin https://github.com/Anagh-007/Anagh-007.git
git push -u origin main
```

## 4. Enable Actions

Go to:

`Settings → Actions → General`

Allow GitHub Actions to run.

The Snake workflow will generate the contribution animation automatically.

## 5. Important

Your GitHub username must be exactly:

`Anagh-007`

If your actual username is different, replace every occurrence of `Anagh-007` in `README.md` and `.github/workflows/snake.yml`.
