# H2HPARSER

This project was developed to parse DOCX files. The application will read the files and extracts relevant information. Once parsed, the app uploads the data to the H2HAPI.

## Build

`git clone https://github.com/mikezm/docx-parser-halfway-to-history.git`
`cd docx-parser-halfway-to-history`
`pip install requirements.txt`

## Run

`./app.py -y <Chapter Year> -c <Chapter Title> -f <Path To DocX File>`  
`./app.py -y 1988 -c "THE WANING OF THE COLD WAR" -f ~/H2HDocs/H2H-chapter-one-1988.docx`  

## Chapter Schema

> **Chapter**  
>     **Title**  
>     **Year**  
>     **Articles** *(array of Class **Article**)*  
>         *Article*   
>             headline *(string)*  
>             speakers *(array of Class **Speaker**)*  
>                 *Speaker*  
>                     name  
>                     affiliation  
>     **Date** *(required)*  
>     **Info texts** *(array of strings)*   
>         text *(string)*  
>     **Content** *(array of Class **Paragraph**)*   
>         *Paragraph*  
>             Text     : *(required)*  
>             Speaker  : *(optional)*  
>             Question : *(optional)*  
>             Comment  : *(True|False)*  
>     **Tags** *(array of tags)*  