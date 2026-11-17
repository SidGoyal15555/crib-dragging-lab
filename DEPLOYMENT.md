# Deployment guide

This project has two deployment targets:

- **Streamlit Community Cloud** runs the interactive Python application (`app.py`).
- **GitHub Pages** serves the static project website from `docs/`.

GitHub Pages cannot execute the Streamlit Python app by itself.

## 1. Push the project to GitHub

Create a public GitHub repository (for example, `crib-dragging-lab`) and push the complete project folder. Keep `app.py`, `core/`, `scoring/`, `tests/`, `requirements.txt`, `.streamlit/`, and `docs/` in the repository root.

Do not commit `.venv/`, secrets, or local environment files.

## 2. Deploy the Streamlit app

1. Sign in to Streamlit Community Cloud with GitHub.
2. Choose **Create app**.
3. Select the repository, branch (`main`), and main file path (`app.py`).
4. Deploy. Streamlit installs packages from `requirements.txt`.
5. Copy the generated public app URL, such as `https://your-app-name.streamlit.app`.

## 3. Connect the GitHub Pages landing page to Streamlit

In `docs/index.html`, replace both occurrences of:

`https://YOUR-APP-NAME.streamlit.app`

with the real Streamlit app URL.

Also replace the generic GitHub links (`https://github.com/`) with the actual repository URL.

Commit and push the changes.

## 4. Enable GitHub Pages

1. Open the repository on GitHub.
2. Go to **Settings → Pages**.
3. Under **Build and deployment**, choose **Deploy from a branch**.
4. Select branch `main` and folder `/docs`.
5. Save. GitHub will display the published Pages URL after deployment finishes.

For a repository named `crib-dragging-lab`, the URL usually looks like:

`https://YOUR-GITHUB-USERNAME.github.io/crib-dragging-lab/`

## 5. Verify

- Open the Pages URL and confirm the landing page loads.
- Click **Launch interactive lab** and confirm it opens the Streamlit app.
- Open the Streamlit app and test the Encryption Lab, Crib Dragging Lab, Automated Attack and Key Recovery pages.
- Run `pytest -q` locally to verify the test suite.

## Important

The landing page contains placeholders until the actual GitHub repository URL and Streamlit app URL are known. Replace them before publishing.
