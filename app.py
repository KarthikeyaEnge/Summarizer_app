import streamlit as st
import re
from simplet5 import SimpleT5
from pypdf import PdfReader
from streamlit_option_menu import  option_menu

#Setting the page config and the sidebar
st.set_page_config(page_title='Synopss',page_icon='book',layout="wide")

#Loading the model

model = SimpleT5()
model.load_model("t5","simplet5-epoch-4-train-loss-0.9785-val-loss-1.5034")



# st.sidebar.image("Group.png",width=40)
# st.sidebar.divider()
st.sidebar.image("synopss.svg",width=250)
with st.sidebar:
 #mode=st.sidebar.selectbox("Select your Choice",["Summarize Text","Summarize Pdf"]);
 mode=option_menu("Main Menu", ["Summarize Text", 'Summarize Pdf'], 
        icons=['alphabet', 'book'], menu_icon="cast", default_index=1)
st.sidebar.markdown('---')
expander=st.sidebar.expander("Team")
with expander:
    st.write("Helen Sahith")
    st.write("Karthikeya Enge")
    st.write("SriCharan Reddy Maroodi")

@st.cache_data 
def summarize(user_input):
     summary=model.predict("summarize:"+user_input)
     return summary

def text_summarization(user_input):
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
       


def pdf_summarization(user_input):
    paras=re.split('\n(?=[A-Z])',user_input)
    left_column, right_column = st.columns(2)
    left_column.title("Key Points")
    right_column.title("Summary")
    right_sum=""
    with left_column:
     st.warning("Creating chunks of pdf to summarize...")
     with st.spinner('Generating Points...'):
        st.success("Generated Points:")
        for para in paras:
          if(len(para.split(' '))<=7):
             st.markdown("### "+str(para))
          elif(len(para.split(' '))<=50):
             st.markdown('- '+str(para)) 
             if(len(para.split(' '))>=20):
                    summ=summarize("summarize:"+para)
                    right_sum=right_sum+" "+summ[0]
          else:
              if(len(para.split(' '))>=180):
                  slen=len(para.split(' '))
                  for i in range(0,slen,180):
                    gen_sum=summarize("summarize:"+para[i:i+180])
                    right_sum=right_sum+" "+gen_sum[0]
                    st.markdown("- "+str(gen_sum[0]))
              else:    
               gen_sum=summarize("summarize:"+para)
               right_sum=right_sum+" "+gen_sum[0]
               st.markdown("- "+str(gen_sum[0]))
    with right_column:
        gen_sum=""
        st.success("Generated Summary:")
        st.write(right_sum+".")
        
                  
                     

@st.cache_data 
def extract_text(index):
    page=reader.pages[index]
    text=page.extract_text()
    return text   



try:
 if(mode=="Summarize Text"):
 
      # Input text area for user input
  st.title("Text Summarization")

  user_input = st.text_area("Enter Text to Summarize",height=300)

# Button to generate summary
  if st.button("Generate Summary"):
      if user_input:
          # Generate summary
          user_input=user_input.replace('\n',' ')
          text_summarization(user_input)
      else:
          st.warning("Please provide some text to summarize.")
   

 else:
      st.title("Pdf Summarization")
      file=st.file_uploader("Upload the Pdf file",type=['pdf'])
      if(file is not None):
          reader=PdfReader(file)
          nupages=len(reader.pages)
          page_number =  st.selectbox('Select a page number to extract text from the pdf:', list(range(1,nupages+1)))
          st.write("Total Number of Pages in the Pdf: ",nupages)
          if(page_number<=nupages):
            text=extract_text(int(page_number)-1)
          with st.expander("View Pdf"):
                st.markdown(text,unsafe_allow_html=True)
          pdf_summarization(text)
except Exception as e:
    st.toast(e)       
