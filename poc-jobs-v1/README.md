# poc-jobs

Jobs-resume-rating
Compare the the resume against multiple jobs descript and genrate the rating 
based on skills and extract the matched text from resume and jobs description.

- flash render template is used to render the html
- using nltk.corpus  to reoved the stopwords (a,an,the ...)
- using client.chat.completions.create to create resume 
    comparision against job descriptions
- display the top 5 skills matched
- 
