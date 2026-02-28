import os
from PIL import Image, ImageDraw, ImageFont
import graphviz

# Fonte e pastas de saída
FONT_PATH = "assets/fonts/arial.ttf"
OUTPUT_CERT_DIR = "output/certificados"
OUTPUT_TREE_DIR = "output/arvores"
os.makedirs(OUTPUT_CERT_DIR, exist_ok=True)
os.makedirs(OUTPUT_TREE_DIR, exist_ok=True)

def generate_certificate(bird, template):
    """
    Gera o certificado final com template PNG/PDF.
    """
    path = os.path.join("assets/certificates", template)
    ext = template.lower().split(".")[-1]

    # Se for PDF, apenas copia para a pasta de saída
    if ext == "pdf":
        output_filename = f"cert_{bird['anilha']}_{template}"
        output_path = os.path.join(OUTPUT_CERT_DIR, output_filename)
        with open(path, "rb") as fsrc:
            with open(output_path, "wb") as fdst:
                fdst.write(fsrc.read())
        return output_path

    # PNG → escreve texto por cima
    base = Image.open(path).convert("RGBA")
    draw = ImageDraw.Draw(base)
    font = ImageFont.truetype(FONT_PATH, 48)
    draw.text((250, 300), f"{bird['name']} ({bird['species']})", fill="black", font=font)
    draw.text((250, 370), f"Anilha: {bird['anilha']}", fill="black", font=font)

    filename = f"cert_{bird['anilha']}_{template}"
    outpath = os.path.join(OUTPUT_CERT_DIR, filename)
    base.save(outpath)
    return outpath

def generate_tree(bird, all_birds):
    """
    Gera uma imagem de árvore genealógica para o pássaro e seus ancestrais.
    Usa Graphviz para criar um PNG do grafo.
    """
    dot = graphviz.Digraph(format="png")
    indexed = {b["anilha"]: b for b in all_birds}

    visited = set()

    def add_node_once(node):
        aid = node["anilha"]
        if aid not in visited:
            visited.add(aid)
            dot.node(aid, f"{node['name']} ({aid})")
        return aid

    def build(node):
        aid = add_node_once(node)
        if node.get("father"):
            fid = node["father"]
            if fid in indexed:
                parent = indexed[fid]
                pid = add_node_once(parent)
                dot.edge(pid, aid)
                build(parent)
        if node.get("mother"):
            mid = node["mother"]
            if mid in indexed:
                parent = indexed[mid]
                pid = add_node_once(parent)
                dot.edge(pid, aid)
                build(parent)

    build(bird)

    filename = f"tree_{bird['anilha']}"
    outpath = os.path.join(OUTPUT_TREE_DIR, filename)
    dot.render(outpath)
    return outpath + ".png"