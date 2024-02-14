import streamlit as st
from simplet5 import SimpleT5

model = SimpleT5()
model.load_model("t5","simplet5-epoch-4-train-loss-0.9785-val-loss-1.5034")

# text_to_summarize="""summarize:Controversial plans to end consultant-led maternity services at Withybush Hospital in Haverfordwest emerged late last year. Â£3m is being spent on new and improved facilities at Glangwili, Carmarthen, as well as a new midwife-led unit at Withybush. The changes will begin on 4 August. The plans have sparked protests. The local patients' watchdog expressed concerns that closing the special care baby unit in Haverfordwest to transfer it all to Carmarthen could put lives at risk. Hundreds gathered outside the Senedd at a demonstration last month. Staff were told of progress on the developments at meetings last week. Consultation ended in May and Hywel Dda health board has insisted the care mothers will receive will be safe. The changes are: A Hywel Dda health board spokesman said building work was on schedule but construction of the Withybush midwife-led unit will not start until obstetric services have transferred to Glangwili to minimise disruption. Changes to paediatric services are expected in October. The spokesman added: "Following a series of meetings with senior paediatric clinical staff it is clear that the timelines for recruitment mean that it is not possible to safely move the service at the beginning of August. "It is imperative that any changes are made safely and therefore changes to paediatric services in Glangwili and Withybush Hospitals will now take place in October and not at the same time as maternity and neonatal service changes."

# """


def summarize(user_input):
     summary=model.predict("summarize:"+user_input)
     return summary



# Streamlit UI
st.title("Text Summarization App")

# Input text area for user input
user_input = st.text_area("Enter Text to Summarize")

# Button to generate summary
if st.button("Generate Summary"):
    if user_input:
        # Generate summary
        user_input=user_input.replace('\n',' ')
        if (len(user_input.split(' '))>300):
            st.warning("Text is too long. Splitting into smaller chunks...")
            arr=[]
            for i in range(0,len(user_input.split(' ')),300):
                arr.append(' '.join(user_input.split(' ')[i:i+300]))
            summary=[]
            with st.spinner('Generating summary...'):
                st.success("Generated Summary:")
                for i in range(0,len(arr)):
                   generated_sum=summarize("summarize:"+arr[i])# Display the generated summary
                   if(summary.count(generated_sum)==0):
                       summary.append(generated_sum[0])
                       st.markdown("- "+str(generated_sum[0]))
        
        else:
            with st.spinner('Generating summary...'):
               summary=summarize("summarize:"+user_input)
        # Display the generated summary
            st.success("Generated Summary:")
            st.write(summary)     
    else:
        st.warning("Please enter some text to summarize.")
