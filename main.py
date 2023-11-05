import cv2
import easyocr
import matplotlib.pyplot as plt
import numpy as np
import re
import json
from flask import Flask
from flask_cors import CORS
app=Flask(__name__)
CORS(app)
@app.route('/path/<pathimg>', methods=['POST'])
# read image
def imgext (pathimg):
    image_path =  pathimg.replace('%', '\\').replace("'", '"')
    img = cv2.imread(r"" +image_path)
    plt.imshow(img, cmap='gray')
    plt.axis('off')
    plt.show()


    langues = ['en' ,'fr' ]  
    utiliser_gpu = False    
    reader = easyocr.Reader(langues, gpu=utiliser_gpu)

    # detect text on image
    text_ = reader.readtext(img)

    threshold = 0.2
    full_text = ''

    # Draw bbox and text
    for t_, t in enumerate(text_):
        bbox, text, score = t

        # Check if the detection score is above the threshold
        if score > threshold:
            pt1 = (int(bbox[0][0]), int(bbox[0][1]))
            pt2 = (int(bbox[2][0]), int(bbox[2][1]))

            # Draw a green rectangle around the detected text region
            cv2.rectangle(img, pt1, pt2, (0, 255, 0), 5)

            # Put the text label in blue near the top-left corner of the detected text region
            cv2.putText(img, text, (int(bbox[0][0]), int(bbox[0][1]) - 10), cv2.FONT_HERSHEY_COMPLEX, 0.65, (255, 0, 0), 2)
            full_text += text + ' '

            # Check if the detected text is "DESIGNATION"
            if text.lower() == "designation" or text.lower() == "désignation" or text.lower() == "degisnation":
                x1, y1, x2, y2 = int(bbox[0][0]), int(bbox[0][1]), int(bbox[2][0]), int(bbox[2][1])

                
                for next_t_ in range(t_ + 1, len(text_)):
                    next_bbox, next_text, next_score = text_[next_t_]

                    if next_score > threshold and abs(next_bbox[0][0] - x1) < 35:  
                        x1 = min(x1, int(next_bbox[0][0]))
                        y2 = int(next_bbox[2][1])

                
                x1 -= 350  #  left
                x2 += 150  # Aright

                # Draw the enlarged red rectangle around the "DESIGNATION"
                cv2.rectangle(img, (x1, y1), (x2, y2), (0, 0, 255), 5)

               
                designations = ''
                for t_ in text_:
                    bbox, text, score = t_
                    x, y = bbox[0]
                    if x1 <= x <= x2 and y1 <= y <= y2:
                        designations += text + ' , '

                

    print(full_text)

    plt.imshow(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
    plt.axis('off')
    plt.show()

    print("red_rectangle :")
    print(designations)



    # Extraction de la date
    date_pattern = r"LE:\s(\d{2}/\d{2}/\d{4})"
    date_match = re.search(date_pattern, full_text)
    date = date_match.group(1) if date_match else None


    # Extraction du premier numéro de téléphone à 8 chiffres
    telephone_pattern_1 = r"\b(\d{8})\b"
    telephone_match_1 = re.search(telephone_pattern_1, full_text)
    telephone_1 = telephone_match_1.group(1) if telephone_match_1 else None

    # Extraction du deuxième numéro de téléphone à 8 chiffres
    telephone_pattern_2 = r"\b(\d{8})\b"
    telephone_match_2 = re.search(telephone_pattern_2, full_text[full_text.index(telephone_1) + 1 :])
    telephone_2 = telephone_match_2.group(1) if telephone_match_2 else None

    # Extraction du mot après "Client" 
    client_pattern = r"(?<=Client\s)\w+"
    client_match = re.search(client_pattern, full_text)
    client = client_match.group() if client_match else None

    # Extraction du total TTC
    total_ttc_pattern = r"TOTAL TTC:\s([\d.]+)"
    total_ttc_match = re.search(total_ttc_pattern, full_text)
    total_ttc = total_ttc_match.group(1) if total_ttc_match else None





    # Étape 3: Stocker les informations extraites dans une liste principale
    result_list = [
        {
            "Date": date,
            "Telephone fournisseur": telephone_1,
            "Telephone Client ": telephone_2,
            "Client": client,
            "Total TTC": total_ttc,
            "designation": designations,
        }
    ]

    # Convertir la liste en format JSON avec une belle présentation (indentation)
    json_data = json.dumps(result_list, indent=4)

    # Enregistrer le fichier JSON dans un fichier
    with open("resultats.json", "w") as json_file:
        json_file.write(json_data)

    return json_file
    

    
var=r"C:\Users\maali\OneDrive\Bureau\test invoice\3.jpg"

#imgext(var)
@app.route('/<PAR>', methods=['POST'])
def test(PAR):
    test=r""
    return  test + PAR.replace('%', '\\')

if __name__ == '__main__':
    app.run(debug=True)