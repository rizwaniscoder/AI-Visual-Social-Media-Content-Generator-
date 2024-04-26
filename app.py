import streamlit as st
from openai import OpenAI
import os
from datetime import datetime
import webbrowser
import requests
# Initialize OpenAI client
openai_api_key = st.text_input("Enter your OpenAI API key:")

openai_client = OpenAI(api_key=openai_api_key)

today = datetime.today()
timestamp = today.strftime('%Y-%m-%d_%H-%M-%S')
filename = f"generated_content_{timestamp}.txt"


def generate_image(prompt):
    response = openai_client.images.generate(
        model="dall-e-3",
        prompt=prompt,
        size="1024x1024",
        quality="standard",
        n=1
    )
    image_url = response.data[0].url

    # Download image
    image_data = requests.get(image_url).content
    image_filename = f"generated_image_{timestamp}.png"
    with open(image_filename, "wb") as img_file:
        img_file.write(image_data)
    
    # Open image URL in a new tab
    webbrowser.open_new_tab(image_url)
    
    return image_url



# Function to generate image prompt
def generate_image_prompt():
    response = openai_client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": """Generate an image prompt related to Next-Generation websites and robots. Basically we are a business and 
             here's what we do: We create AI NexGen websites and robots—In the dynamic realm of technology, our website and robot developers are at the forefront of developing innovative, high-impact business solutions
             Here is an example prompt but use your imagination to generate more creative prompts. And don't take more than 50 percent from this prompt: 'A futuristic, dynamic image illustrating the urgency of upgrading to a Next-Generation website. The scene shows a sleek, modern website interface with advanced features, holographic elements, and high-speed data streams. In the background, blurred images of outdated websites lag behind, symbolizing the risk of falling behind in the digital race. The central focus is a bold, eye-catching countdown timer, indicating the limited time available to stay ahead. Bright arrows and speed lines emphasize the concept of rapid progress and staying ahead of the competition in the online business world. The overall atmosphere is high-tech, urgent, and forward-thinking, conveying the message that immediate action is necessary to maintain a competitive edge on the Internet'"""},
        ]
    )
    return response.choices[0].message.content

# Function to generate caption for Instagram
def generate_instagram_caption(semantics):
    response = openai_client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": f"A futuristic image illustrating the urgency of upgrading to a Next-Generation website. The scene shows {semantics}. Make sure to add hashtags and emojis."},
        ]
    )
    return response.choices[0].message.content

# Function to generate caption for Twitter
def generate_twitter_caption(semantics):
    response = openai_client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": f"A dynamic image emphasizing the need for innovative Next-Generation websites and robots. The scene depicts {semantics}. Keep it different from the Instagram caption, add social value to it. Make sure to add hashtags and emojis."},
        ]
    )
    return response.choices[0].message.content

# Function to generate caption for LinkedIn
def generate_linkedin_caption(semantics):
    response = openai_client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": f"A professional image highlighting the importance of embracing Next-Generation technology. The scene portrays {semantics}. Keep it professional, add social value to it. Make sure to add proper hashtags and emojis."},
        ]
    )
    return response.choices[0].message.content

# Function to generate caption for Facebook
def generate_facebook_caption(semantics):
    response = openai_client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": f"An engaging image showcasing the transformative power of Next-Generation websites and robots. The scene features {semantics}. Add social value to it. Make sure to add proper hashtags and emojis."},
        ]
    )
    return response.choices[0].message.content

# Main Streamlit app
def main():
    st.title("Autonomous Social Media Content Generator")
    st.markdown("### Business Overview for WebsitesAndRobots.com\nWebsitesAndRobots.com creates AI NexGen websites and robots. Our developers fuse expertise and cutting-edge AI technology to revolutionize businesses' operations.")

    # Generate image prompt
    user_prompt = st.text_area("Enter an image generation prompt (optional)")

    # Generate image prompt if user doesn't provide one
    if not user_prompt:
        generate_image_prompt_btn = st.button("Generate Image Prompt")
        if generate_image_prompt_btn:
            st.info("Generating image prompt...")
            st.session_state.image_prompt = generate_image_prompt()
            st.success("Image prompt generated successfully!")
            st.write("Generated Image Prompt:")
            st.write(st.session_state.image_prompt)
    else:
        st.session_state.image_prompt = user_prompt

    # Generate image
    generate_image_btn = st.button("Generate Image")
    if generate_image_btn:
        if 'image_prompt' not in st.session_state:
            st.error("Please generate image prompt first!")
        else:
            st.info("Generating image...")
            st.session_state.image_url = generate_image(st.session_state.image_prompt)
            st.success("Image generated successfully!")
            st.image(st.session_state.image_url, caption="Generated Image", use_column_width=True)


    # Generate captions for different platforms
    generate_captions_btn = st.button("Generate Captions")
    if generate_captions_btn:
        if 'image_prompt' not in st.session_state:
            st.error("Please generate image prompt first!")
        else:
            st.info("Generating captions...")
            st.session_state.instagram_caption = generate_instagram_caption(st.session_state.image_prompt)
            st.session_state.twitter_caption = generate_twitter_caption(st.session_state.image_prompt)
            st.session_state.linkedin_caption = generate_linkedin_caption(st.session_state.image_prompt)
            st.session_state.facebook_caption = generate_facebook_caption(st.session_state.image_prompt)

            st.write("#### Instagram Caption:")
            st.write(st.session_state.instagram_caption)

            st.write("#### Twitter Caption:")
            st.write(st.session_state.twitter_caption)

            st.write("#### LinkedIn Caption:")
            st.write(st.session_state.linkedin_caption)

            st.write("#### Facebook Caption:")
            st.write(st.session_state.facebook_caption)

    # Sidebar to show generated image and captions
    st.sidebar.title("Generated Results")

    if 'image_url' in st.session_state:
        st.sidebar.markdown("## Generated Image")
        st.sidebar.image(st.session_state.image_url, caption="Generated Image", use_column_width=True)

    if 'instagram_caption' in st.session_state:
        st.sidebar.markdown("## Captions")
        st.sidebar.write("#### Instagram Caption:")
        st.sidebar.write(st.session_state.instagram_caption)

    if 'twitter_caption' in st.session_state:
        st.sidebar.write("#### Twitter Caption:")
        st.sidebar.write(st.session_state.twitter_caption)

    if 'linkedin_caption' in st.session_state:
        st.sidebar.write("#### LinkedIn Caption:")
        st.sidebar.write(st.session_state.linkedin_caption)

    if 'facebook_caption' in st.session_state:
        st.sidebar.write("#### Facebook Caption:")
        st.sidebar.write(st.session_state.facebook_caption)
        
    # Download the result
    download_btn = st.button("Download Results")
    if download_btn:
        with open(filename, "w") as f:
            f.write(f"Image Prompt:\n{st.session_state.image_prompt}\n\n")
            if 'image_url' in st.session_state:
                f.write(f"Image URL:\n{st.session_state.image_url}\n\n")
            if 'instagram_caption' in st.session_state:
                f.write(f"Instagram Caption:\n{st.session_state.instagram_caption}\n\n")
            if 'twitter_caption' in st.session_state:
                f.write(f"Twitter Caption:\n{st.session_state.twitter_caption}\n\n")
            if 'linkedin_caption' in st.session_state:
                f.write(f"LinkedIn Caption:\n{st.session_state.linkedin_caption}\n\n")
            if 'facebook_caption' in st.session_state:
                f.write(f"Facebook Caption:\n{st.session_state.facebook_caption}")

        # Provide direct download link
        with open(filename, "rb") as f:
            data = f.read()
        st.download_button(label="Download Results By Clicking Here", data=data, file_name=filename)

if __name__ == "__main__":
    main()
