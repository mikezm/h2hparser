# H2HPARSER

This project was developed to parse DOCX files. The application will read the files and extracts relevant information. Once parsed, the app uploads the data to the H2HAPI.

## Install

`git clone https://github.com/mikezm/h2hparser.git`  
`cd h2hparser`  
`pip install -r requirements.txt`  

## Usage

`python ./app.py -y <Chapter Year> -c <Chapter Title> -f <Path To DocX File>`  
`python ./app.py -y 1988 -c "THE WANING OF THE COLD WAR" -f ~/H2HDocs/H2H-chapter-one-1988.docx`  

## Chapter Schema

*   **Chapter**
    *   **Title** *(string)*
    *   **Year** *(string)*
    *   **Articles** *(array of Class **Article**)*
        *   ***Article***
            *   Headline *(string)*
            *   Speakers *(array of Class **Speaker**)*
                *   *Speaker*
                    *   name        : *(string)*
                    *   affiliation : *(string)*
    *   **Date** *(Datetime)*
    *   **Information** *(array of strings)*
    *   **Content** *(array of Class **Paragraph**)*
        *   ***Paragraph***
            *   Text     : *(string)*
            *   Speaker  : *(Class **Speaker**)*
            *   Question : *(boolean)*
            *   Comment  : *(boolean)*
    *   **Tags** *(array of strings)*