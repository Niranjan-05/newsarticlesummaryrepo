import openai
from flask import Flask, render_template, request



##  DD's key
#openai.api_key = "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"

##  nsj's key
openai.api_key = "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"

application = Flask(__name__)

from getlinks2 import *
links = fetch_links('https://www.gulf-times.com/')
links = list(set(links))
dit = extraction(links,'sanjay1111.txt')

#print('int')
int_links = fetch_links('https://www.gulf-times.com/international')
int_links = list(set(int_links))
#print('listssssssssssssss',int_links)
int_dit = extraction(int_links,'sanjayint.txt')

delete_duplicates(dit,int_dit)

#print('buss')
bussiness_links = fetch_links('https://www.gulf-times.com/business')
bussiness_links = list(set(bussiness_links))
bussiness_dit = extraction(bussiness_links,'sanjaybussiness.txt')

delete_duplicates(dit,bussiness_dit)
delete_duplicates(int_dit,bussiness_dit)


#print('sport')
sports_links = fetch_links('https://www.gulf-times.com/sport')
sports_links = list(set(sports_links))
sports_dit = extraction(sports_links,'sanjaysport.txt')

delete_duplicates(dit,bussiness_dit)
delete_duplicates(int_dit,bussiness_dit)
delete_duplicates(sports_dit,bussiness_dit)

f = open('sanjay1111.txt', 'rb')
k = f.read()
k1 = k.decode('utf8')

headlines = dit.keys()
int_headlines = int_dit.keys()
business_headlines = bussiness_dit.keys()
sports_headlines = sports_dit.keys()

#print(headlines)
#print('int')
#print(int_headlines)
#print('business')
#print(business_headlines)
#print('sports')
#print(sports_headlines)


@application.route("/")
def index():
    return render_template("index.html", headlines=headlines,int_headlines=int_headlines,business_headlines=business_headlines, sports_headlines=sports_headlines)

dit1 = dit.copy()
dit1.update(int_dit)
dit1.update(bussiness_dit)
dit1.update(sports_dit)
@application.route("/summary", methods=["POST"])
def summarize():
    # Get the selected headline from the form data
    selected_headline = request.form["headline"]

    # Get the user's desired summary length from the form data
    summary_length = int(request.form["max_length"])
    #print(summary_length)

    # Use OpenAI API to summarize the selected headline
    #print(dit1[selected_headline])
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=dit1[selected_headline] + "\n\nSummary:",
        max_tokens=summary_length,
        n=1,
        stop=None,
        temperature=0.5
    )

    # Extract the generated summary from the API response
    summary = response.choices[0].text.strip().replace("Summary:", "")
    #print('ssummary_is')
    #print(summary)
    # Render the summary template with the generated summary
    return render_template("summary.html", headline=selected_headline, summary=summary)

if __name__ == "__main__":
    application.run(debug=True)
