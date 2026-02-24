# Portfolio #2: Shopping Workflow at SauceDemo

## Description
This project demonstrates a structured test architecture covering end-to-end process navigation across 
multiple interconnected pages. It focuses on verifying business-critical flow logic, maintaining
clean separation of responsibilities and improving readability of pytest test through a custom wrapper.

## Tech Stack
- Python 3.14, Selenium WebDriver, Conftest + Pytest
- ChromeDriver, WebDriver Manager

## Webpage
- SauceDemo : https://www.saucedemo.com/

## Features
1. Login authentication and inventory page validation.
2. Add, remove, and clear shopping cart item verification.
3. Page transition detection through dynamic header assertion.
4. Wrapper to standardize test invocation and reduce repetitive logic.

## Challenges
- Inconsistent header rendering timing across page transitions.
- Unexpected browser alert prompts handled via Chrome preferences configuration.
- Extract numerical values from mixed DOM elements.

## Setup & Run
1. Clone the repository to your local machine
   - git clone https://github.com/SomethingAddUp/Handbook-2.git
   - cd Handbook-2
2. Install dependencies required for the tests
   - pip install -r requirements.txt
3. Run automated tests
   - pytest
