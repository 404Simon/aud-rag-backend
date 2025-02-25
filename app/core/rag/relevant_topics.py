import ell
from pydantic import BaseModel, Field

ell.init(store="./logdir", autocommit=True)


class RelevantTopics(BaseModel):
    elementare_datentypen: bool = Field(
        description="Dieses Teilgebiet der Informatik beschäftigt sich mit **elementaren Datenstrukturen**, die in Programmiersprachen verwendet werden. Es werden **verschiedene Datentypen** wie Ganzzahlen, Fließkommazahlen, boolesche Werte, Zeichen und Zeichenketten vorgestellt. Darüber hinaus werden **Datenstrukturen** wie Aufzählungen, Datensätze, Felder, Listen und dynamische Datenstrukturen, einschließlich verketteter Listen, erläutert. Das Dokument **erklärt auch das Konzept des abstrakten Datentyps (ADT)** und gibt Beispiele für Speicherstrukturen wie Stapel, Warteschlangen und Prioritätswarteschlangen."
    )
    algorithmenbewertung_und_laufzeit: bool = Field(
        description="Das Teilgebiet befasst sich mit der **Komplexitätstheorie**, die sich mit der Bewertung der Effizienz von Algorithmen beschäftigt. Es werden **verschiedene Methoden zur Effizienzberechnung** vorgestellt, von der Zeitmessung bis zur asymptotischen Abschätzung. Das Dokument erklärt die **Bedeutung der Komplexitätsklassen** wie linear, polynomiell und exponentiell, und diskutiert die **Problemklassen P, NP, NP-schwer und NP-vollständig**. Anhand von **Beispielen wie Fibonacci-Zahlen, Feldern, Matrizen und dem Springerproblem** wird die Anwendung der Komplexitätstheorie veranschaulicht."
    )
    graphen_baeume: bool = Field(
        description="**Graphen und Bäumen sind fundamentale Datenstrukturen in der Informatik**. Sie behandeln **grundlegende Definitionen, Eigenschaften und verschiedene Arten dieser Strukturen**, wie z.B. gerichtete und ungerichtete Graphen, Bäume, Wurzelbäume und Binärbäume. Darüber hinaus werden **Algorithmen zur Verarbeitung von Graphen und Bäumen** vorgestellt, darunter Suchalgorithmen (Breitensuche, Tiefensuche), Algorithmen zur Berechnung von minimalen Spannbäumen (Prim, Kruskal) und Algorithmen zur Bestimmung kürzester Wege (Dijkstra, Floyd)."
    )
    sortierung: bool = Field(
        description="Diese Lektion befasst sich mit **Sortieralgorithmen**, die in verschiedene Kategorien eingeteilt werden, darunter einfache, schnelle, spezielle und externe Verfahren. Sie beschreiben die **Funktionsweise verschiedener Algorithmen wie Bubble Sort, Selection Sort, Insertion Sort, Shell Sort, Heap Sort, Quick Sort, Merge Sort und Counting Sort**, analysieren ihre Laufzeitkomplexität und vergleichen ihre Effizienz in unterschiedlichen Szenarien."
    )
    suchen: bool = Field(
        description="**Suchalgorithmen in Feldern und Bäumen** mit Fokus auf binäre Suchbäume und AVL-Bäume. Sie lernen verschiedene Suchmethoden, darunter lineare und binäre Suche sowie Interpolationssuche, und beschreiben **die Funktionsweise, Komplexität und Vor- und Nachteile** der jeweiligen Verfahren. Weiterhin werden **B-Bäume als plattenbasierte Suchstruktur** vorgestellt und die Unterschiede zu B*-Bäumen, die eine effizientere Speicherung und Organisation großer Datenmengen ermöglichen, erläutert. Im zweiten Teil wird außerdem **Hashing als Verfahren zur schnellen Suche** vorgestellt."
    )
    codierung: bool = Field(
        description="Die Codierung bietet eine umfassende Einführung in das Thema Codierung in der Informatik und behandelt verschiedene Aspekte wie **grundlegende Definitionen, Code-Erzeugung, Code-Sicherung, lineare Codes und nicht-binäre Codes**. Es werden **etablierte Codierungsverfahren** wie BCD, ASCII und Unicode vorgestellt sowie **Methoden zur Fehlererkennung und -korrektur** wie Paritätscodes, Kreuzparität und Hamming-Distanz erläutert. Das Dokument beinhaltet zudem **zahlreiche Beispiele und Übungsaufgaben** zur Vertiefung des Verständnisses."
    )
    kompression: bool = Field(
        description="Die Lektion Datenkompression stellt verschiedene Kompressionsverfahren vor, darunter die arithmetische Codierung, Lauflängencodierung, Differenzcodierung und den LZW-Algorithmus. Es werden **sowohl verlustfreie als auch verlustbehaftete Kompressionsmethoden** erklärt und anhand von Beispielen illustriert."
    )

    def get_document_title_filterpatterns(self) -> list[str]:
        patterns = []

        if self.elementare_datentypen:
            patterns.extend(["%AlgorithmenAusHamsterbuch%", "%01_Elementare%"])

        if self.algorithmenbewertung_und_laufzeit:
            patterns.append("%02_AlgoBewertung%")

        if self.graphen_baeume:
            patterns.extend(["%03_Graphen%", "%04_Baeume%", "%_GraphAlgo%"])

        if self.sortierung:
            patterns.extend(["%_Sortieren%"])

        if self.suchen:
            patterns.extend(["%_Suchen%"])

        if self.codierung:
            patterns.append("%14_Codierung%")

        if self.kompression:
            patterns.append("%15_Kompression%")

        return patterns


@ell.complex(model="gpt-4o-mini", response_format=RelevantTopics)
def find_relevant_topics(question: str) -> RelevantTopics:
    """
    Du bist Informatikexperte.
    Analysiere die gegebene Frage und bestimme alle relevanten Teilgebiete der Informatik.
    """
    return f"Frage: {question}"


def main():
    question = "Gegeben sei der gerichtete Graph G = ({1,2,3,4,5,6,7}, {(1,2), (1,3), (2,5), (2,4), (3,4), (4,7),  (5,6), (6,7)}). Ist der Graph planar darstellbar? Zeichne ihn!"
    print(find_relevant_topics(question).parsed.get_document_title_filterpatterns())


if __name__ == "__main__":
    main()
