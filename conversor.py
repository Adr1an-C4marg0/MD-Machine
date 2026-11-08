import re
import unicodedata
import xml.etree.ElementTree as ET

ARQ_XML = r"C:\Users\Adria\Downloads\players_list_xml\players_list_xml_foa.xml"
SAIDA = "base.pl"
TOP_N = 500


def norm(s):
    s = unicodedata.normalize("NFKD", s)
    s = "".join(c for c in s if not unicodedata.combining(c))
    return re.sub(r"[^a-z0-9]+", "_", s.lower()).strip("_")


def nome_normal(s):
    if "," in s:
        sobrenome, nome = s.split(",", 1)
        s = nome + " " + sobrenome
    return norm(s)


def inteiro(txt):
    try:
        return int(txt)
    except (TypeError, ValueError):
        return None


jogadores = []

for p in ET.parse(ARQ_XML).getroot().findall("player"):
    classico = inteiro(p.findtext("rating"))
    rapido = inteiro(p.findtext("rapid_rating"))
    blitz = inteiro(p.findtext("blitz_rating"))
    ano = inteiro(p.findtext("birthday"))
    nome = p.findtext("name")
    pais = p.findtext("country")
    sexo = p.findtext("sex")
    titulo = p.findtext("title")

    if None in (classico, rapido, blitz, ano) or not (nome and pais and sexo and titulo):
        continue

    jogadores.append((nome_normal(nome), norm(pais), norm(sexo), ano,
                      norm(titulo), classico, rapido, blitz))

jogadores.sort(key=lambda j: j[5], reverse=True)

with open(SAIDA, "w", encoding="utf-8") as f:
    for j in jogadores[:TOP_N]:
        f.write("jogador({}, {}, {}, {}, {}, {}, {}, {}).\n".format(*j))

print(len(jogadores[:TOP_N]), "jogadores gravados em", SAIDA)