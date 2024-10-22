import streamlit as st
from PIL import Image
import requests

# Dictionary containing information for all diseases
DISEASE_INFO = {
    "Apple Aphis spp": {
        "impact": "Reduces tree vigor, distorts leaves and fruit, can transmit viruses.",
        "symptoms": "Curled or distorted leaves, sticky honeydew on leaves and fruit, presence of small green, red, or black insects.",
        "lifecycle": "Eggs overwinter on bark, hatch in spring. Multiple generations occur throughout growing season.",
        "cause": "Infestation by various species of aphids belonging to the genus Aphis.",
        "prevention": "Encourage beneficial insects, use reflective mulches, prune to improve air circulation.",
        "recommended_action": "Apply insecticidal soaps or neem oil, introduce natural predators like ladybugs, remove heavily infested parts."
    },
    "Apple Erisosoma lanigerum": {
        "impact": "Damages roots and branches, reduces tree vigor and yield.",
        "symptoms": "White, woolly masses on bark, branches, and roots; cankers and galls on woody tissues.",
        "lifecycle": "Overwinters as nymphs on roots or bark crevices. Multiple generations per year.",
        "cause": "Infestation by the woolly apple aphid (Eriosoma lanigerum).",
        "prevention": "Plant resistant rootstocks, maintain tree health, encourage beneficial insects.",
        "recommended_action": "Prune and destroy infested branches, apply horticultural oils, use systemic insecticides if severe."
    },
    "Apple Monillia laxa": {
        "impact": "Causes blossom blight, twig cankers, and fruit rot, reducing yield and fruit quality.",
        "symptoms": "Brown, wilted blossoms; cankers on twigs and branches; brown, rotting fruit with fungal spores.",
        "lifecycle": "Overwinters in cankers, infects blossoms in spring, spreads to fruit and twigs.",
        "cause": "Infection by the fungus Monilinia laxa.",
        "prevention": "Prune for good air circulation, remove mummified fruit, apply dormant sprays.",
        "recommended_action": "Remove and destroy infected plant parts, apply fungicides during bloom and fruit development."
    },
    "Apple Venturia inaequalis": {
        "impact": "Reduces fruit quality and yield, can defoliate trees if severe.",
        "symptoms": "Olive-green to black spots on leaves and fruit; scabby, corky areas on fruit.",
        "lifecycle": "Overwinters in fallen leaves, releases spores in spring to infect new growth.",
        "cause": "Infection by the fungus Venturia inaequalis.",
        "prevention": "Choose resistant varieties, improve air circulation, rake and destroy fallen leaves.",
        "recommended_action": "Apply fungicides preventatively, starting at bud break and continuing through the growing season."
    },
    "Apricot Coryneum beijerinckii": {
        "impact": "Causes fruit spotting, twig cankers, and potentially tree death if severe.",
        "symptoms": "Small, round purple spots on fruit that become raised and corky; sunken cankers on twigs.",
        "lifecycle": "Overwinters in twig cankers, spreads by water splash in spring and summer.",
        "cause": "Infection by the fungus Coryneum beijerinckii.",
        "prevention": "Prune for good air circulation, avoid overhead irrigation, apply copper sprays in autumn.",
        "recommended_action": "Remove and destroy infected twigs, apply fungicides during bud break and petal fall."
    },
    "Apricot Monillia laxa": {
        "impact": "Causes blossom blight, twig dieback, and fruit rot, reducing yield significantly.",
        "symptoms": "Brown, wilted blossoms; cankers on twigs; brown, rotting fruit with fungal spores.",
        "lifecycle": "Overwinters in cankers and mummified fruit, infects blossoms in spring, spreads to fruit.",
        "cause": "Infection by the fungus Monilinia laxa.",
        "prevention": "Remove mummified fruit, prune for air circulation, apply dormant sprays.",
        "recommended_action": "Remove and destroy infected plant parts, apply fungicides during bloom and fruit development."
    },
    "Cancer symptom": {
        "impact": "Can lead to branch dieback, reduced vigor, and potentially tree death if untreated.",
        "symptoms": "Sunken, discolored areas on bark; cracking or peeling bark; branch dieback.",
        "lifecycle": "Varies depending on the specific pathogen causing the cancer.",
        "cause": "Various pathogens including bacteria and fungi, often entering through wounds.",
        "prevention": "Maintain tree health, avoid wounding, sterilize pruning tools, use proper pruning techniques.",
        "recommended_action": "Remove affected branches, apply appropriate fungicides or bactericides based on the specific pathogen."
    },
    "Cherry Aphis spp": {
        "impact": "Reduces tree vigor, distorts leaves, can transmit viruses.",
        "symptoms": "Curled or distorted leaves, sticky honeydew on leaves and fruit, presence of small insects.",
        "lifecycle": "Eggs overwinter on bark, hatch in spring. Multiple generations occur throughout growing season.",
        "cause": "Infestation by various species of aphids affecting cherry trees.",
        "prevention": "Encourage beneficial insects, use reflective mulches, prune to improve air circulation.",
        "recommended_action": "Apply insecticidal soaps or neem oil, introduce natural predators, remove heavily infested parts."
    },
    "Downy mildew": {
        "impact": "Reduces photosynthesis, can cause defoliation and reduced yield.",
        "symptoms": "Yellow spots on upper leaf surfaces, fuzzy gray-purple growth on lower leaf surfaces.",
        "lifecycle": "Overwinters in plant debris, spreads by wind and water in cool, humid conditions.",
        "cause": "Infection by various species of oomycete fungi, depending on the host plant.",
        "prevention": "Improve air circulation, avoid overhead watering, plant resistant varieties.",
        "recommended_action": "Remove infected plants or plant parts, apply fungicides preventatively in high-risk conditions."
    },
    "Drying symptom": {
        "impact": "Can lead to reduced plant vigor, yield loss, and potentially plant death if severe.",
        "symptoms": "Wilting, browning, or drying of leaves, stems, or entire plants.",
        "lifecycle": "Varies depending on the underlying cause of the drying symptom.",
        "cause": "Various factors including drought, root damage, vascular diseases, or environmental stress.",
        "prevention": "Proper irrigation, soil management, and plant care to maintain overall plant health.",
        "recommended_action": "Identify and address the underlying cause (e.g., improve watering, treat for diseases, adjust environmental conditions)."
    },
    "Gray mold": {
        "impact": "Causes fruit rot, blossom blight, and stem cankers, reducing yield and quality.",
        "symptoms": "Gray, fuzzy mold on fruits, flowers, and stems; soft, rotting tissue.",
        "lifecycle": "Overwinters on plant debris, infects during cool, wet conditions.",
        "cause": "Infection by the fungus Botrytis cinerea.",
        "prevention": "Improve air circulation, avoid plant crowding, reduce humidity, handle plants carefully to avoid wounds.",
        "recommended_action": "Remove and destroy infected plant parts, apply fungicides during flowering and fruit development."
    },
    "Leaf scars": {
        "impact": "Generally not harmful, but can be entry points for pathogens if damaged.",
        "symptoms": "Marks on stems where leaves were previously attached.",
        "lifecycle": "Occurs naturally as part of the plant's growth and leaf shedding process.",
        "cause": "Natural process of leaf abscission and shedding.",
        "prevention": "Not necessary as this is a natural process.",
        "recommended_action": "No action needed unless wounds are excessive or showing signs of infection."
    },
    "Peach Monillia laxa": {
        "impact": "Causes blossom blight, twig dieback, and fruit rot, reducing yield significantly.",
        "symptoms": "Brown, wilted blossoms; cankers on twigs; brown, rotting fruit with fungal spores.",
        "lifecycle": "Overwinters in cankers and mummified fruit, infects blossoms in spring, spreads to fruit.",
        "cause": "Infection by the fungus Monilinia laxa.",
        "prevention": "Remove mummified fruit, prune for air circulation, apply dormant sprays.",
        "recommended_action": "Remove and destroy infected plant parts, apply fungicides during bloom and fruit development."
    },
    "Peach Parthenolecanium corni": {
        "impact": "Reduces tree vigor, produces honeydew that leads to sooty mold, can weaken branches.",
        "symptoms": "Brown, helmet-shaped scales on branches; sticky honeydew; sooty mold on leaves and fruit.",
        "lifecycle": "Overwinters as nymphs, matures in spring, produces one generation per year.",
        "cause": "Infestation by the European fruit lecanium scale (Parthenolecanium corni).",
        "prevention": "Maintain tree health, encourage natural predators, avoid excessive nitrogen fertilization.",
        "recommended_action": "Prune and destroy heavily infested branches, apply horticultural oils during dormant season."
    },
    "Pear Erwinia amylovora": {
        "impact": "Causes rapid blighting of blossoms, shoots, and branches, can kill entire trees.",
        "symptoms": "Blackened blossoms, leaves, and twigs; bacterial ooze; shepherd's crook appearance of shoots.",
        "lifecycle": "Overwinters in cankers, spreads via insects and rain in spring.",
        "cause": "Infection by the bacterium Erwinia amylovora.",
        "prevention": "Plant resistant varieties, maintain tree health, avoid excessive nitrogen, prune properly.",
        "recommended_action": "Remove and destroy infected plant parts, apply copper-based bactericides during bloom."
    },
    "Plum Aphis spp": {
        "impact": "Reduces tree vigor, distorts leaves, can transmit viruses.",
        "symptoms": "Curled or distorted leaves, sticky honeydew on leaves and fruit, presence of small insects.",
        "lifecycle": "Eggs overwinter on bark, hatch in spring. Multiple generations occur throughout growing season.",
        "cause": "Infestation by various species of aphids affecting plum trees.",
        "prevention": "Encourage beneficial insects, use reflective mulches, prune to improve air circulation.",
        "recommended_action": "Apply insecticidal soaps or neem oil, introduce natural predators, remove heavily infested parts."
    },
    "RoughBark": {
        "impact": "Can indicate underlying stress or disease, may provide entry points for pathogens.",
        "symptoms": "Rough, cracked, or peeling bark on tree trunks or branches.",
        "lifecycle": "Varies depending on the underlying cause of the rough bark.",
        "cause": "Various factors including environmental stress, age, or certain diseases.",
        "prevention": "Maintain overall tree health, protect from environmental stresses, avoid trunk injuries.",
        "recommended_action": "Identify and address underlying causes, protect exposed wood if necessary, consult an arborist if severe."
    },
    "StripeCanker": {
        "impact": "Can girdle branches or trunks, reducing tree vigor and potentially causing death.",
        "symptoms": "Elongated, sunken cankers on branches or trunks, often with a striped appearance.",
        "lifecycle": "Varies depending on the specific pathogen causing the canker.",
        "cause": "Various fungal pathogens, often entering through wounds or natural openings.",
        "prevention": "Maintain tree health, avoid wounding, practice proper pruning techniques.",
        "recommended_action": "Remove infected branches, apply appropriate fungicides, protect pruning wounds."
    },
    "Walnut Eriophyies erineus": {
        "impact": "Causes leaf distortion and reduced photosynthesis, but generally not severe.",
        "symptoms": "Small, rounded galls on upper leaf surfaces; corresponding depressions on lower surfaces.",
        "lifecycle": "Overwinters in buds, becomes active in spring, multiple generations per year.",
        "cause": "Infestation by the walnut leaf gall mite (Eriophyes erineus).",
        "prevention": "Maintain tree health, encourage natural predators of mites.",
        "recommended_action": "Pruning affected leaves, applying horticultural oils or sulfur-based products if severe."
    },
    "Walnut Gnomonialeptostyla": {
        "impact": "Causes early defoliation, reduces nut quality and yield.",
        "symptoms": "Brown spots on leaves, often along veins; early leaf drop; dark spots on nuts.",
        "lifecycle": "Overwinters in fallen leaves, releases spores in spring to infect new growth.",
        "cause": "Infection by the fungus Gnomonia leptostyla (also known as Ophiognomonia leptostyla).",
        "prevention": "Rake and destroy fallen leaves, improve air circulation, apply dormant sprays.",
        "recommended_action": "Apply fungicides preventatively, starting at bud break and continuing through the growing season."
    }
}

def get_disease_info(disease_name):
    return DISEASE_INFO.get(disease_name, {
        "impact": "Information not available.",
        "symptoms": "Information not available.",
        "lifecycle": "Information not available.",
        "cause": "Information not available.",
        "prevention": "Information not available.",
        "recommended_action": "Information not available."
    })

def main():
    st.sidebar.title("Navigation")
    page = st.sidebar.radio("Go to", ["Disease Prediction", "About Product", "About Developer"])

    if page == "Disease Prediction":
        disease_prediction_page()
    elif page == "About Product":
        about_product_page()
    elif page == "About Developer":
        about_developer_page()

def disease_prediction_page():
    st.title("Plant Disease Detection")

    uploaded_file = st.file_uploader("Choose an image", type=["jpg", "jpeg", "png"])

    if uploaded_file is not None:
        image = Image.open(uploaded_file)
        st.image(image, caption='Uploaded Image', use_column_width=True)
        
        byte_img = uploaded_file.getvalue()
        response = requests.post("http://localhost:8001/predict", files={"file": byte_img})
        
        if response.status_code == 200:
            prediction = response.json()["predicted_disease"]
            st.write(f"Predicted disease: {prediction}")
            
            disease_info = get_disease_info(prediction)
            
            st.subheader("Disease Information")
            st.write(f"**Impact:** {disease_info['impact']}")
            st.write(f"**Symptoms:** {disease_info['symptoms']}")
            st.write(f"**Lifecycle:** {disease_info['lifecycle']}")
            st.write(f"**Cause:** {disease_info['cause']}")
            st.write(f"**Prevention:** {disease_info['prevention']}")
            st.write(f"**Recommended Action:** {disease_info['recommended_action']}")
        else:
            st.write(f"Error: {response.status_code} - {response.text}")
    else:
        st.write("Please upload an image for disease detection.")

def about_product_page():
    st.title("About Our Plant Disease Detection Product")
    
    st.write("""
    Our Plant Disease Detection product is an advanced AI-powered tool designed to help farmers, 
    gardeners, and plant enthusiasts identify and manage plant diseases quickly and accurately.
    
    Key Features:
    1. Fast and accurate disease detection
    2. Comprehensive information on impact, symptoms, lifecycle, cause, prevention, and recommended actions
    3. Support for multiple plant species
    4. User-friendly interface
    
    How it works:
    1. Upload a photo of the affected plant
    2. Our AI model analyzes the image
    3. Receive instant results with disease identification and detailed information
    """)
    
    st.subheader("Diseases Our Model Can Predict")
    for disease in DISEASE_INFO.keys():
        st.write(f"- {disease}")

def about_developer_page():
    st.title("About the Developer")
    
    st.write("""
    This Plant Disease Detection application was developed by [Data Drifters].
    
    We are passionate about leveraging technology to solve real-world problems in agriculture 
    and plant care. Our team consists of experts in machine learning, plant pathology, and 
    software development.
    
    Our mission is to make plant disease detection accessible and easy for everyone, from 
    professional farmers to home gardeners.
    
    If you have any questions, suggestions, or feedback, please don't hesitate to contact us at:
    [Your Contact Information]
    
    Thank you for using our application!
    """)

if __name__ == "__main__":
    main()