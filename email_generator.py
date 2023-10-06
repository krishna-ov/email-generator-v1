import json

from dotenv import load_dotenv
from langchain.schema import SystemMessage, HumanMessage
from langchain.chat_models import ChatOpenAI

load_dotenv()

def generate_email(prompt):
    model = ChatOpenAI(
        model_name='gpt-3.5-turbo',
        temperature=0.1, 
        max_tokens=400, 
        streaming=True
    )
    
    email_sample = model(prompt)

    return email_sample.content


def prepare_prompt(company_title, company_founder, company_information):
    
    system_template = """You are Gabrielle an helpful associate on the investment team at OpenView working to source and evaluate new investment opportunities.
With the company information, you need craft an email(including any interesting things like funding, awards or milestones from the company information to catch the founders eye) to the founder of that company stating that we are interested in investing in the company and why we are interested.

#### Sample:
Hi Paul,

I recently came across Hedge and am super interested in what you’re building and how you're giving users a suite of apps that's purpose built for video to increase the efficiencies across all stages of the video workflow.  Congrats on all the success you’ve seen so far!

By way of an intro - I work at OpenView a $2B venture firm based out of Boston.  We focus in B2B software and have invested in companies like Datadog, Calendly, and Expensify.

I completely understand fundraising may not be top of mind right now, but I'd love to learn more about Hedge and what's to come.  If you're open to it, I'd love to connect later this week or next for a quick intro call.  Happy to work around your schedule to make something work!

Best,
Gabrielle
####

"""

    human_template = """
Here's the company information you want to use for crafting the email.
Mention any interesting thing like funding, awards or milestones from the company information to catch the founders eye. 
=====================
Title: {company_title}

{company_founder}

{company_information}
====================
Don't mention about the amount we are investing. We are just letting the founder know we are interested and inviting the founder for a call or a meeting to discuss further.
"""

    human_prompt = human_template.format(company_title=company_title, company_founder=company_founder, company_information=company_information)


    messages = [
        SystemMessage(content=system_template),
        HumanMessage(content=human_prompt)
    ]

    return messages


def generate_sample(company_name=None, company_founder=None, company_information=None):
    # If a company_name is provided, load the JSON data and extract the company details
    # If only a company_name is provided (and not the other details), load the JSON data and extract the company details
    if company_name and not (company_name and company_founder and company_information):
        with open('companies_info.json', 'r') as f:
            data = json.load(f)
            companies = data['companies']
            company = next((comp for comp in companies.values() if comp['name'] == company_name), None)
            company_name = company['name']
            company_founder = company['founder']
            company_information = company['description']

    prompt = prepare_prompt(company_title=company_name, company_founder=company_founder, company_information=company_information) 

    generated_email = generate_email(prompt)

    return generated_email
