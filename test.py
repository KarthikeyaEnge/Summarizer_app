import streamlit as st
from simplet5 import SimpleT5
from pypdf import PdfReader
st.set_page_config(layout="wide")

#Loading the model

model = SimpleT5()
model.load_model("t5","simplet5-epoch-4-train-loss-0.9785-val-loss-1.5034")


#Setting the page config and the sidebar

# st.sidebar.image("Group.png",width=40)
# st.sidebar.divider()
mode=st.sidebar.selectbox("Select your Choice",["Summarize Text","Summarize Pdf"]);




def summarize(user_input):
     summary=model.predict("summarize:"+user_input)
     return summary

def summarization(user_input):
    if (len(user_input.split(' '))>300):
            st.warning("Text is too long. Splitting into smaller chunks...")
            arr=[]
            for i in range(0,len(user_input.split(' ')),150):
                arr.append(' '.join(user_input.split(' ')[i:i+150]))
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
            st.write(summary[0])     
   

def extract_text(file):
    # with open(file,'r') as f:
            # reader=PdfReader(f)
            # page=reader.pages[0]
            # text=page.extract_text()

    reader=PdfReader(file)
    page=reader.pages[0]
    text=page.extract_text()
    return text        


if(mode=="Summarize Text"):
     # Input text area for user input
 st.title("Text Summarization")
 user_input = st.text_area("Enter Text to Summarize",height=300)

# Button to generate summary
 if st.button("Generate Summary"):
    if user_input:
        # Generate summary
        user_input=user_input.replace('\n',' ')
        summarization(user_input)
    else:
        st.warning("Please provide some text to summarize.")
  

else:
    st.title("Pdf Summarization")
    file=st.file_uploader("Upload the Pdf file",type=['pdf'])
    if(file is not None):
        text=extract_text(file)
        st.write(text)
        summarization(text)