# H2HPARSER

This project was developed to parse DOCX files. The application will read the files and extracts relevant information. Once parsed, the app uploads the data to the H2HAPI.

## Build

`git clone https://github.com/mikezm/docx-parser-halfway-to-history.git`
`cd docx-parser-halfway-to-history`
`pip install requirements.txt`

## Run

`>> ./app.py -y <Chapter Year> -c <Chapter Title> -f <Path To DocX File>`
`>> ./app.py -y 1988 -c "THE WANING OF THE COLD WAR" -f ~/H2HDocs/H2H-chapter-one-1988.docx`

## Schema

Chapter
  - Title
  - Year
  - Articles (array of Class Article)
    -- Article --
    -- headline (required)
    -- speakers (required)
      --- Speaker ---
      --- name
      --- affiliation
    -- date (required)
    -- info texts (optional)
      -- text ---
    -- content (array of paragraphs)
      --- Paragraph ---
      --- text (required)
      --- speaker :: <BOLD-Name>: (optional)
      --- Question :: <BOLD>Q: (optional)
      --- Comment (True|False)
    -- tags (array of tags)