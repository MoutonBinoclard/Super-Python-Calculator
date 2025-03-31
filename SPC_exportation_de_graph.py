import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import to_hex, to_rgb
from matplotlib.offsetbox import OffsetImage, AnnotationBbox
from datetime import datetime
import  json
import os
import matplotlib.font_manager as fm


font_path = "SPC_fonts/Rubik.ttf"
custom_font = fm.FontProperties(fname=font_path)

classement1={'E9AB8EFC5BEC7D47': ['Fifur', 79.65301672790822, [15.837516198992207, 18.691347676681186, 3.7844428289691403, 15.273487206818858, 8.973185572692172, 17.093037243754665]], '19E28695724AFD95': ['The extensive axolotl', 78.46948200172424, [9.999418045564527, 17.270055702217203, 4.976352017959336, 14.879956236763025, 18.55741192279543, 12.786288076424725]], '924945A68F8A0E7A': ['three evil babies + trenchcoat', 65.0321503551618, [17.38652761234051, 5.786564260666861, 14.98686818966806, 11.06248492926853, 4.660190977968753, 11.149514385249093]], '54E426DBA416133': ['med0iqyt', 61.271546483027, [4.342132269276718, 7.402209950489416, 21.804087793162548, 8.432944719774312, 12.123302013254175, 7.166869737069835]], '7C1569D98EDC54D': ['Incrpt.99r    ', 43.965465995914805, [6.066517316235388, 14.556997088911675, 10.823047775495889, 4.983610543812587, 4.104574395336355, 3.4307188761229117]], '337BAB47093D6036': ['SF)Sc0rv4™', 38.62933516327864, [5.564641829989908, 6.313861767754103, 7.717343558298278, 0, 16.226016642808585, 2.8074713644277667]], 'FF4DB3B319ECED7D': ['SNX | ψNafyψ ♡', 38.0624468555155, [15.227221105502624, 6.290434522715423, 5.564641829989908, 4.081810597077202, 5.166817086281979, 1.7315217139483656]], '4E07A6F41B5F65E8': ['SNX | HaWk_Youtube ?', 28.263506009366292, [1.988927345848041, 1.7076773724355663, 15.227221105502624, 1.407830435489036, 1.9468928869127096, 5.984956863178317]], '88B6D1EA6C063276': ['33"@kcl', 23.616452699821217, [12.458225598683782, 0, 0, 0, 4.825032539972404, 6.3331945611650315]], '2BDAFEF855174022': ['F∀$〒☆ρφ†ε', 23.42782357186141, [2.8221896443917176, 4.070176393499229, 5.717298988697336, 5.137615633269391, 5.680542912003737, 0]], '53F9EFB9912B04AE': ['TTV Mouton Binoclard', 22.147453276966168, [7.258426505225584, 4.700708297495616, 1.2347474712040385, 3.227284435056216, 3.4795759801265267, 2.2467105878581863]], '383E3EC66B0A4EFF': ['CottncandyYT', 19.22556883665947, [0, 1.3179434794707152, 4.271001833114289, 12.13105420132676, 1.5055693227477067, 0]], '625B2698F0B0A74': ['roro', 12.755604700869855, [5.717298988697336, 5.434348493750589, 1.6039572184219297, 0, 0, 0]], '40A1795F6A574169': ['MoyaGT0102', 11.580998898600468, [2.3933246220557898, 3.010904592062312, 2.3933246220557898, 3.7834450624265763, 0, 0]], '83C16BD4221C3D0C': ['Neko', 11.142248974586865, [0, 0, 6.624206756542966, 4.518042218043899, 0, 0]], '7398964898705DAB': ['leveling', 7.2330411739735005, [0, 0, 2.8221896443917176, 4.410851529581783, 0, 0]], 'D1043FE3E6680799': ['♀Νιηησυ²', 4.152277282885299, [1.6039572184219297, 2.548320064463369, 0, 0, 0, 0]], '815A3B77F74D9E41': ['Himiclawe★', 1.2347474712040385, [1.2347474712040385, 0, 0, 0, 0, 0]]}
dictionnaire_ID={'53F9EFB9912B04AE': [[7, 1, 15, False, -1, 1], [7, 0, 14, False, -1, 0], [15, 0, 15, False, -1, 0], [9, 0, 13, False, -1, 0], [8, 0, 12, False, -1, 0], [9, 0, 10, False, -1, 0]], '54E426DBA416133': [[8, 0, 15, False, -1, 0], [4, 0, 14, False, -1, 0], [1, 4, 15, True, -1, 4], [3, 0, 13, False, -1, 0], [3, 2, 12, False, -1, 2], [5, 1, 10, False, -1, 1]], 'FF4DB3B319ECED7D': [[2, 2, 15, False, -1, 2], [12, 2, 14, False, -1, 2], [10, 1, 15, False, -1, 1], [12, 1, 13, False, -1, 1], [9, 1, 12, False, -1, 1], [10, 0, 10, False, -1, 0]], '2BDAFEF855174022': [[11, 0, 15, False, -1, 0], [8, 0, 14, False, -1, 0], [6, 0, 15, False, -1, 0], [6, 0, 13, False, -1, 0], [5, 0, 12, False, -1, 0], [0, 0, 0, False, -1, 0]], '7C1569D98EDC54D': [[9, 1, 15, False, -1, 1], [3, 3, 14, False, -1, 3], [5, 2, 15, False, -1, 2], [10, 1, 13, False, -1, 1], [7, 0, 12, False, -1, 0], [7, 0, 10, False, -1, 0]], '815A3B77F74D9E41': [[15, 0, 15, False, -1, 0], [0, 0, 0, False, -1, 0], [0, 0, 0, False, -1, 0], [0, 0, 0, False, -1, 0], [0, 0, 0, False, -1, 0], [0, 0, 0, False, -1, 0]], 'D1043FE3E6680799': [[14, 0, 15, False, -1, 0], [11, 0, 14, False, -1, 0], [0, 0, 0, False, -1, 0], [0, 0, 0, False, -1, 0], [0, 0, 0, False, -1, 0], [0, 0, 0, False, -1, 0]], '4E07A6F41B5F65E8': [[13, 0, 15, False, -1, 0], [13, 0, 14, False, -1, 0], [2, 2, 15, False, -1, 2], [13, 0, 13, False, -1, 0], [11, 0, 12, False, -1, 0], [4, 0, 10, False, -1, 0]], '337BAB47093D6036': [[10, 1, 15, False, -1, 1], [5, 0, 14, False, -1, 0], [4, 0, 15, False, -1, 0], [0, 0, 0, False, -1, 0], [2, 3, 12, True, -1, 3], [8, 0, 10, False, -1, 0]], '924945A68F8A0E7A': [[3, 4, 15, True, -1, 4], [9, 1, 14, False, -1, 1], [3, 3, 15, False, -1, 3], [5, 2, 13, True, -1, 2], [10, 1, 12, False, -1, 1], [3, 2, 10, False, -1, 2]], '625B2698F0B0A74': [[6, 0, 15, False, -1, 0], [6, 0, 14, False, -1, 0], [14, 0, 15, False, -1, 0], [0, 0, 0, False, -1, 0], [0, 0, 0, False, -1, 0], [0, 0, 0, False, -1, 0]], '19E28695724AFD95': [[4, 1, 15, False, -1, 1], [1, 2, 14, False, -1, 2], [7, 0, 15, False, -1, 0], [1, 1, 13, False, -1, 1], [1, 3, 12, True, -1, 3], [2, 2, 10, False, -1, 2]], 'E9AB8EFC5BEC7D47': [[1, 1, 15, False, -1, 1], [2, 4, 14, True, -1, 4], [9, 0, 15, False, -1, 0], [2, 2, 13, True, -1, 2], [4, 1, 12, False, -1, 1], [1, 3, 10, True, -1, 3]], '88B6D1EA6C063276': [[5, 3, 15, False, -1, 3], [0, 0, 0, False, -1, 0], [0, 0, 0, False, -1, 0], [0, 0, 0, False, -1, 0], [6, 0, 12, False, -1, 0], [6, 1, 10, False, -1, 1]], '40A1795F6A574169': [[12, 0, 15, False, -1, 0], [10, 0, 14, False, -1, 0], [12, 0, 15, False, -1, 0], [8, 0, 13, False, -1, 0], [0, 0, 0, False, -1, 0], [0, 0, 0, False, -1, 0]], '383E3EC66B0A4EFF': [[0, 0, 0, False, -1, 0], [14, 0, 14, False, -1, 0], [13, 1, 15, False, -1, 1], [4, 2, 13, True, -1, 2], [12, 0, 12, False, -1, 0], [0, 0, 0, False, -1, 0]], '83C16BD4221C3D0C': [[0, 0, 0, False, -1, 0], [0, 0, 0, False, -1, 0], [8, 1, 15, False, -1, 1], [11, 1, 13, False, -1, 1], [0, 0, 0, False, -1, 0], [0, 0, 0, False, -1, 0]], '7398964898705DAB': [[0, 0, 0, False, -1, 0], [0, 0, 0, False, -1, 0], [11, 0, 15, False, -1, 0], [7, 0, 13, False, -1, 0], [0, 0, 0, False, -1, 0], [0, 0, 0, False, -1, 0]]}

color_scheme = "SPC_color_schemes/SPC_cs_v4.json"

def charger_couleurs(fichier=color_scheme): # Charger les couleurs depuis le fichier JSON
    with open(fichier, "r", encoding="utf-8") as f:
        return json.load(f)

# Charger les couleurs
couleurs = charger_couleurs()

nom_du_tournoi = "Super Python Calculator, By Mouton"

logo=False

# This is where you can change the path to the logo file:
logo_path = "SPC_logo/SPC_lg_trio_troubles.png"

# Size of the logo
zoom_logo=0.15

# If you want the date to show up on the graph, set the following value to True:
date=True

# Appliquer les couleurs
couleur_du_titre = couleurs["couleur_du_titre"]
couleur_date = couleurs["couleur_date"]
couleur_de_fond = couleurs["couleur_de_fond"]
couleur1 = couleurs["couleur1"]
couleur2 = couleurs["couleur2"]
couleur3 = couleurs["couleur3"]
couleur4 = couleurs["couleur4"]
nombre_choisi = couleurs["nombre_choisi"]
couleur_label_x = couleurs["couleur_label_x"]
couleur_label_y = couleurs["couleur_label_y"]
couleur_axe_x = couleurs["couleur_axe_x"]
couleur_axe_y = couleurs["couleur_axe_y"]
couleur_points = couleurs["couleur_points"]
couleur_contour_legende = couleurs["couleur_contour_legende"]
couleur_texte_legende = couleurs["couleur_texte_legende"]
couleur_fliers = couleurs["couleur_fliers"]
couleur_caps = couleurs["couleur_caps"]
couleur_whiskers = couleurs["couleur_whiskers"]
couleur_boxes_inside = couleurs["couleur_boxes_inside"]
couleur_boxes_outside = couleurs["couleur_boxes_outside"]
couleur_medians = couleurs["couleur_medians"]
couleur_moyenne = couleurs["couleur_moyenne"]
couleur_horizontales = couleurs["couleur_horizontales"]



def generer_degrade_4_couleurs(couleur1, couleur2, couleur3, couleur4, nombre_de_couleurs): #Couleur sous le format #xxxxxx et nombre de couleur 7 modulo 3+

    # Convertir les couleurs hexadécimales en RGB
    rgb1 = to_rgb(couleur1)
    rgb2 = to_rgb(couleur2)
    rgb3 = to_rgb(couleur3)
    rgb4 = to_rgb(couleur4)

    # Créer un tableau de valeurs pour interpoler entre les couleurs
    t = np.linspace(0, 1, nombre_de_couleurs)

    # Interpoler linéairement entre les quatre couleurs
    degrade = []
    for i in t:
        if i <= 0.333:
            # Interpolation entre couleur1 et couleur2
            r = rgb1[0] + (rgb2[0] - rgb1[0]) * (i * 3)
            g = rgb1[1] + (rgb2[1] - rgb1[1]) * (i * 3)
            b = rgb1[2] + (rgb2[2] - rgb1[2]) * (i * 3)
        elif i <= 0.666:
            # Interpolation entre couleur2 et couleur3
            r = rgb2[0] + (rgb3[0] - rgb2[0]) * ((i - 0.333) * 3)
            g = rgb2[1] + (rgb3[1] - rgb2[1]) * ((i - 0.333) * 3)
            b = rgb2[2] + (rgb3[2] - rgb2[2]) * ((i - 0.333) * 3)
        else:
            # Interpolation entre couleur3 et couleur4
            r = rgb3[0] + (rgb4[0] - rgb3[0]) * ((i - 0.666) * 3)
            g = rgb3[1] + (rgb4[1] - rgb3[1]) * ((i - 0.666) * 3)
            b = rgb3[2] + (rgb4[2] - rgb3[2]) * ((i - 0.666) * 3)
        
        # Clipper les valeurs RGB entre 0 et 1
        r = max(0, min(1, r))
        g = max(0, min(1, g))
        b = max(0, min(1, b))
        
        # Convertir la couleur RGB en hexadécimal et l'ajouter à la liste
        degrade.append(to_hex((r, g, b)))

    return degrade








def exporter_graph(classement):  # Génère le graph du classement à partir d'un dico classement

     # définir le score max du graph pour ajuster le spacing des scores
    le_haut_du_graph = next(iter(classement.values()))[1]

    # définir la couleur des barres
    barres_couleurs = generer_degrade_4_couleurs(couleur1, couleur2, couleur3, couleur4, nombre_choisi) # Augmenter le nombre de couleurs par trois
    
    # Créer un graphique en barres empilées avec un style personnalisé
    plt.figure(figsize=(12, 6), facecolor=couleur_de_fond)
    ax = plt.gca()  # Obtenir l'axe actuel
    
    # Fond pour l'arrière-plan du graphique
    ax.set_facecolor(couleur_de_fond)

    # Pour stocker les handles de la légende
    legend_handles = []

    # Pour chaque joueur, empiler les scores de chaque manche
    for i, (playfab_id, data) in enumerate(classement.items()):
        pseudo, score_final, scores_manches = data
        # Troncature du pseudo s'il dépasse 15 caractères
        if len(pseudo) > 17:
            pseudo = pseudo[:15] + "..."
        bottom = 0  # Commencer à empiler à partir de 0
        for j, score in enumerate(scores_manches):
            bar = plt.bar(pseudo, score, bottom=bottom, color=barres_couleurs[j % len(barres_couleurs)])
            bottom += score  # Mettre à jour la position de départ pour la prochaine manche

            # Ajouter un handle pour la légende (une seule fois par manche)
            if i == 0:  # On ne le fait que pour le premier joueur pour éviter les doublons
                legend_handles.append(bar[0])

        # Ajouter le score total en haut de la barre, en vertical et empiétant sur les colonnes
        plt.text(pseudo, score_final + 0.03*le_haut_du_graph, f"{score_final:.2f}", ha='center', va='bottom', color=couleur_points, fontsize=10, rotation=90, fontproperties=custom_font)

    
    # Utiliser les graduations automatiques de Matplotlib pour les lignes horizontales
    y_ticks = ax.get_yticks()  # Récupérer les positions des graduations sur l'axe Y
    for y in y_ticks:
        ax.axhline(y, color=couleur_horizontales, linestyle='--', linewidth=0.5, zorder=0)  # Ajouter une ligne horizontale à chaque graduation

    # Changer la couleur des ticks (graduations) et des labels de l'axe X
    ax.tick_params(axis='x', which='both', colors=couleur_axe_x)
    ax.xaxis.label.set_color(couleur_label_x)

    # Changer la couleur des ticks (graduations) et des labels de l'axe Y
    ax.tick_params(axis='y', which='both', colors=couleur_axe_y)
    ax.yaxis.label.set_color(couleur_label_y)
   
    # Désactiver les bordures du haut et de la droite
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)

    # Garder les bordures gauche et basse visibles
    ax.spines['left'].set_visible(True)
    ax.spines['bottom'].set_visible(True)

    # Définir la couleur des axes X et Y
    ax.spines['bottom'].set_color(couleur_axe_x)
    ax.spines['left'].set_color(couleur_axe_y)

    # Rotation des noms des joueurs pour une meilleure lisibilité avec une taille de police réduite
    plt.xticks(rotation=45, ha='right', fontsize=8, color=couleur_label_x, fontproperties=custom_font)  # Correction de la couleur des ticks X avec police custom_font
    plt.yticks(color=couleur_label_y, fontproperties=custom_font)  # Correction de la couleur et de la police des ticks Y

    # Ajouter une légende
    labels = [f"Round {i+1}" for i in range(len(barres_couleurs))]  # Créer les labels pour chaque manche
    legend = plt.legend(legend_handles, labels, title_fontsize='large', fontsize='medium', facecolor=couleur_de_fond, edgecolor=couleur_contour_legende, labelcolor=couleur_texte_legende, prop=custom_font)

    # Ajuster la mise en page
    plt.tight_layout()

    # Ajouter des marges à gauche et à droite pour plus de légèreté
    plt.subplots_adjust(left=0.15, right=0.85, top=0.82)

    # Ajout d'un titre
    plt.title(nom_du_tournoi, fontdict={'color': couleur_du_titre, 'fontsize': 16, 'weight': 'bold', 'fontproperties': custom_font}, pad=20)  # Gestion du titre avec police custom_font

    if logo == True:
        # Charger le logo
        logo_image = plt.imread(logo_path)

        # Ajouter le logo à la place du titre
        ax = plt.gca()
        image_box = OffsetImage(logo_image, zoom=zoom_logo)  # Ajuster le zoom pour auto-scaling
        annotation_box = AnnotationBbox(image_box, (0.5, 1.065), xycoords='axes fraction', frameon=False, box_alignment=(0.5, 0))
        ax.add_artist(annotation_box)
        ax.set_title("")

    if date == True:
        # Ajouter la date du jour comme titre, mais descendre la position
        today_date = datetime.now().strftime("%d/%m/%Y")
        ax.text(0.5, 1.05, today_date, transform=ax.transAxes, ha='center', va='top', fontdict={'color': couleur_date, 'fontsize': 8, 'fontproperties': custom_font})

    # Afficher le graphiques
    plt.show()


    # Enregistrer le graphique
    #plt.savefig(os.path.join("SPC_exports", "SPC_Graphic.png"), dpi=600, facecolor=couleur_de_fond)


exporter_graph(classement1)