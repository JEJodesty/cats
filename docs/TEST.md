## [Test(s)](../tests/verification_test.py):
* **[Install CATs](https://github.com/BlockScience/cats/tree/cats2?tab=readme-ov-file#get-started)**
* **[Create Virtual Environment](./ENV.md)**
* **Activate Virtual Environment**
  ```bash
  cd cats
  source ./venv/bin/activate
  # (venv) $
  ```
* **Session 1**
  ```bash
  # (venv) $
  PYTHONPATH=./ python cats/node.py
  ```
* **List Tests** without running them:
  ```bash
  # (venv) $
  pytest --collect-only tests/verification_test.py
  ```

* **Session 2:** *Run All Tests*
  ```bash
  # (venv) $
  pytest -s tests/verification_test.py
  ```