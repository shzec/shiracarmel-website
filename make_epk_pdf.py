from pathlib import Path
from io import BytesIO
from PIL import Image as PILImage
from reportlab.lib import colors
from reportlab.lib.enums import TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import mm
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image, Table, TableStyle, PageBreak
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

ROOT = Path(__file__).parent
OUT = ROOT / "assets" / "epk-shira-z-carmel.pdf"
PAPER = colors.HexColor("#f8f4eb")
INK = colors.HexColor("#211e1a")
WINE = colors.HexColor("#7d263d")
MUTED = colors.HexColor("#645d53")
pdfmetrics.registerFont(TTFont("DejaVuSans", "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"))
pdfmetrics.registerFont(TTFont("DejaVuSans-Bold", "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"))
pdfmetrics.registerFont(TTFont("DejaVuSerif", "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"))
pdfmetrics.registerFont(TTFont("DejaVuSerif-Bold", "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"))
styles = getSampleStyleSheet()
styles.add(ParagraphStyle(name="Kicker", parent=styles["Normal"], fontName="DejaVuSans-Bold", fontSize=7, leading=10, textColor=WINE, spaceAfter=4))
styles.add(ParagraphStyle(name="Hero", parent=styles["Title"], fontName="DejaVuSerif-Bold", fontSize=34, leading=32, textColor=INK, alignment=TA_LEFT, spaceAfter=7))
styles.add(ParagraphStyle(name="Sub", parent=styles["Normal"], fontName="DejaVuSans", fontSize=8, leading=12, textColor=MUTED))
styles.add(ParagraphStyle(name="H2x", parent=styles["Heading2"], fontName="DejaVuSerif-Bold", fontSize=19, leading=21, textColor=INK, spaceBefore=2, spaceAfter=7))
styles.add(ParagraphStyle(name="Bodyx", parent=styles["BodyText"], fontName="DejaVuSans", fontSize=8.5, leading=12.6, textColor=INK, spaceAfter=6))
styles.add(ParagraphStyle(name="Smallx", parent=styles["BodyText"], fontName="DejaVuSans", fontSize=7.2, leading=10, textColor=MUTED))
styles.add(ParagraphStyle(name="CellTitle", parent=styles["Normal"], fontName="DejaVuSerif-Bold", fontSize=11, leading=14, textColor=INK))
styles.add(ParagraphStyle(name="Linkline", parent=styles["Normal"], fontName="DejaVuSans", fontSize=7.6, leading=11, textColor=WINE, spaceAfter=0))
styles.add(ParagraphStyle(name="PoemText", parent=styles["BodyText"], fontName="DejaVuSerif", fontSize=10.5, leading=15, textColor=INK, alignment=TA_LEFT))
styles.add(ParagraphStyle(name="Divider", parent=styles["Normal"], fontName="DejaVuSans-Bold", fontSize=11, leading=14, textColor=colors.HexColor("#1e5551"), alignment=1))
styles.add(ParagraphStyle(name="CreditName", parent=styles["Normal"], fontName="DejaVuSans-Bold", fontSize=7.7, leading=11, textColor=WINE))
styles.add(ParagraphStyle(name="CenterSub", parent=styles["Sub"], alignment=1, fontSize=8.8, leading=12, textColor=INK))
styles.add(ParagraphStyle(name="ArtistName", parent=styles["Normal"], fontName="DejaVuSerif-Bold", fontSize=18, leading=22, alignment=1, textColor=INK, spaceAfter=3))
styles.add(ParagraphStyle(name="CenterSmall", parent=styles["Smallx"], alignment=1, fontSize=7, leading=10))
styles.add(ParagraphStyle(name="CenterKicker", parent=styles["Kicker"], alignment=1))
styles.add(ParagraphStyle(name="CompactArtist", parent=styles["Normal"], fontName="DejaVuSerif-Bold", fontSize=20, leading=23, textColor=INK, spaceAfter=2))
styles.add(ParagraphStyle(name="CompactSub", parent=styles["Normal"], fontName="DejaVuSans", fontSize=8, leading=11, textColor=MUTED))
styles.add(ParagraphStyle(name="CompactTitle", parent=styles["Normal"], fontName="DejaVuSerif-Bold", fontSize=15, leading=17, textColor=INK, spaceAfter=3))
styles.add(ParagraphStyle(name="CompactSongTitle", parent=styles["Normal"], fontName="DejaVuSerif-Bold", fontSize=17, leading=19, textColor=INK, spaceAfter=4))
styles.add(ParagraphStyle(name="CompactBody", parent=styles["BodyText"], fontName="DejaVuSans", fontSize=7.5, leading=10.2, textColor=INK, spaceAfter=4))
styles.add(ParagraphStyle(name="CompactSmall", parent=styles["BodyText"], fontName="DejaVuSans", fontSize=6.7, leading=9, textColor=MUTED, spaceAfter=2))
styles.add(ParagraphStyle(name="CompactPoem", parent=styles["BodyText"], fontName="DejaVuSerif", fontSize=8.6, leading=11.4, textColor=INK, alignment=TA_LEFT))
styles.add(ParagraphStyle(name="CompactCredit", parent=styles["Normal"], fontName="DejaVuSans-Bold", fontSize=6.5, leading=8.3, textColor=WINE))
styles.add(ParagraphStyle(name="CompactCreditValue", parent=styles["Normal"], fontName="DejaVuSans", fontSize=6.5, leading=8.3, textColor=MUTED))

def compressed_image(path, size=(1100, 1100)):
    source = PILImage.open(path)
    if "A" in source.getbands():
        background = PILImage.new("RGBA", source.size, (248, 244, 235, 255))
        background.alpha_composite(source.convert("RGBA"))
        image = background.convert("RGB")
    else:
        image = source.convert("RGB")
    image.thumbnail(size)
    stream = BytesIO()
    image.save(stream, "JPEG", quality=84, optimize=True)
    stream.seek(0)
    return stream

def para(text, style="Bodyx"):
    return Paragraph(text, styles[style])

def frame(canvas, doc):
    canvas.saveState()
    canvas.setFillColor(PAPER)
    canvas.rect(0, 0, A4[0], A4[1], stroke=0, fill=1)
    canvas.setStrokeColor(colors.HexColor("#c9b9a7"))
    canvas.setLineWidth(.45)
    canvas.line(17*mm, 14*mm, A4[0]-17*mm, 14*mm)
    canvas.setFont("Helvetica", 6.5)
    canvas.setFillColor(MUTED)
    canvas.drawString(17*mm, 9*mm, "SHIRA Z. CARMEL  ·  ELECTRONIC PRESS KIT")
    canvas.drawRightString(A4[0]-17*mm, 9*mm, f"{doc.page:02d}")
    canvas.restoreState()

doc = SimpleDocTemplate(str(OUT), pagesize=A4, rightMargin=17*mm, leftMargin=17*mm, topMargin=12*mm, bottomMargin=19*mm, title="Shira Z. Carmel — Electronic Press Kit", author="Shira Z. Carmel")
story = []
logo = Image(compressed_image(ROOT / "assets" / "artist-mark-name.png", (700, 700)), width=25*mm, height=25*mm)
masthead = Table([[logo, [para("Shira Z. Carmel", "CompactArtist"), para("Composer · Singer · Songwriter", "CompactSub")]]], colWidths=[32*mm,139*mm])
masthead.setStyle(TableStyle([("VALIGN",(0,0),(-1,-1),"MIDDLE"),("LEFTPADDING",(0,0),(-1,-1),0),("RIGHTPADDING",(0,0),(-1,-1),0),("TOPPADDING",(0,0),(-1,-1),0),("BOTTOMPADDING",(0,0),(-1,-1),0)]))
release_description = "A stark chamber song for voice, cello, baritone saxophone and piano that leaves Tal Nitzán’s chilling poem exposed and confronts listeners with motherhood, moral responsibility and the blurred line between victim and perpetrator."
short_bio = "Shira Z. Carmel is a Jerusalem-born, Melbourne-based composer, singer and songwriter. Performing in English, Hebrew and Yiddish, she moves between jazz, cabaret, folk, alternative pop and experimental song, often setting poetry to music. Her work spans film, radio, interdisciplinary art, television and commercials; her projects have toured internationally. Carmel's new single, “Four Boys Maybe Five,” sets a chilling poem by Tal Nitzán for voice, cello, baritone saxophone and piano. She holds a degree in vocal performance from the Multidisciplinary Department of the Jerusalem Academy of Music and Dance. In 2023, she received the Neve Schechter and Rabinovich Foundation Award for Original Israeli Creation."
cover = Image(compressed_image(ROOT / "assets" / "four-boys-cover.png", (900, 900)), width=43*mm, height=43*mm)
cover.hAlign = "CENTER"
left_column = [
    para("NEW SINGLE", "Kicker"),
    para("Four Boys Maybe Five", "CompactTitle"),
    para("A poem by Tal Nitzán · Music by Shira Z. Carmel", "CompactSmall"),
    Spacer(1, 1.5*mm), cover, Spacer(1, 2*mm),
    para(release_description, "CompactBody"),
    para("·", "Divider"),
    para('<link href="https://too.fm/fbmf" color="#7d263d">LISTEN TO THE SONG: too.fm/fbmf</link>', "Linkline"),
    para('<link href="https://shiracarmel.com/epk.html#press-preview" color="#7d263d"><u>Press Download With Password (WAV file)</u></link>', "Linkline"),
    Spacer(1, 3*mm), para("SHORT BIO", "Kicker"), para(short_bio, "CompactBody")
]
poem = "Four boys, maybe five, are shaking a car,<br/>their faces distorted by the thrill of destruction.<br/>Beneath its wheels lies an abyss.<br/>Inside the car is your son.<br/>The car tilts.<br/>Desolation all around,<br/>desolation within you and without trying<br/>you already know,<br/>no voice will emerge from your throat.<br/>What will you do?<br/><br/>Four boys, maybe five, are shaking a car.<br/>Under its wheels lies an abyss.<br/>The boy in the car is not your son.<br/>Your son is outside with them,<br/>his face distorted by the<br/>thrill of destruction.<br/>What will you do"
song_column = [
    para("THE SONG", "Kicker"),
    para("Four Boys Maybe Five", "CompactSongTitle"),
    para("Poem by Tal Nitzán (originally in Hebrew)<br/>English-language poem published in The Guardian<br/>Recorded and produced in Melbourne", "CompactSmall"),
    Spacer(1, 1.5*mm), para(poem, "CompactPoem"), Spacer(1, 3*mm),
    para("SONG CREDITS", "Kicker")
]
credits = Table([
    [para("Music, voice, arrangement, production:", "CompactCredit"), para("Shira Z. Carmel", "CompactCreditValue")],
    [para("Cello and cello solo:", "CompactCredit"), para("Vincent Ward", "CompactCreditValue")],
    [para("Baritone saxophone:", "CompactCredit"), para("Gideon Brazil", "CompactCreditValue")],
    [para("Piano:", "CompactCredit"), para("Adrian Banner", "CompactCreditValue")],
    [para("Recording, co-production:", "CompactCredit"), para("Dan Shani at Evoke Sounds studios Melbourne", "CompactCreditValue")]
], colWidths=[44*mm, 43*mm])
credits.setStyle(TableStyle([("VALIGN",(0,0),(-1,-1),"TOP"),("LINEBELOW",(0,0),(-1,-2),.35,colors.HexColor("#d6c8b8")),("LEFTPADDING",(0,0),(-1,-1),0),("RIGHTPADDING",(0,0),(-1,-1),1.5*mm),("TOPPADDING",(0,0),(-1,-1),1*mm),("BOTTOMPADDING",(0,0),(-1,-1),1*mm)]))
song_column += [credits]
def column_height(items, width):
    measure = Table([[items]], colWidths=[width])
    measure.setStyle(TableStyle([("LEFTPADDING",(0,0),(-1,-1),0),("RIGHTPADDING",(0,0),(-1,-1),0),("TOPPADDING",(0,0),(-1,-1),0),("BOTTOMPADDING",(0,0),(-1,-1),0)]))
    return measure.wrap(width, 10000)[1]
extra_gap = max(0, column_height(left_column, 77*mm) - column_height(song_column, 89*mm))
if extra_gap:
    song_column.insert(-2, Spacer(1, extra_gap))
first_page = Table([[left_column, "", song_column]], colWidths=[77*mm, 5*mm, 89*mm])
first_page.setStyle(TableStyle([("VALIGN",(0,0),(-1,-1),"TOP"),("LEFTPADDING",(0,0),(-1,-1),0),("RIGHTPADDING",(0,0),(-1,-1),0),("TOPPADDING",(0,0),(-1,-1),0),("BOTTOMPADDING",(0,0),(-1,-1),0)]))
story += [masthead, Spacer(1, 4*mm), first_page, PageBreak(), para("ABOUT THE ARTIST", "Kicker"), para("Long bio", "H2x")]
long_bio = "For more than two decades, Israeli-born and Melbourne-based artist Shira Z. Carmel has made songs that move between alternative pop, jazz, cabaret, folk and experimental music. A composer, singer and songwriter, she works in Hebrew, English and Yiddish, and has built a varied body of work through vocal ensembles, jazz projects, theatrical song and collaborations across the arts. Her music often interweaves political and humanist themes, drawing on her lifelong work as an activist and volunteer.<br/><br/>Shira was a founding member, songwriter and co-arranger of the vocal trio The Hazelnuts, which toured internationally. Other projects include the Shira Z. Carmel Quartet, her brass band Shira Z. Carmel and her Brasserie, the Yiddish experimental duo The Technicalities, and “Infinity and One — Lullabies for Mothers,” a project setting poetry about motherhood to music. Her work has also appeared in film, television, radio and commercials.<br/><br/>She holds a degree in vocal performance from the Multidisciplinary Department of the Jerusalem Academy of Music and Dance. In 2023, she received the Neve Schechter and Rabinovich Foundation Award for Original Israeli Creation.<br/><br/>Her latest single, “Four Boys Maybe Five,” sets a poem by Tal Nitzán in a minimal chamber arrangement for voice, cello, baritone saxophone and piano. The poem’s two mirrored scenes ask a parent to imagine both sides of a violent encounter. Recorded and produced in Melbourne, the song arrives from a distance that offers space to listen closely without looking away."
story += [para(long_bio), Spacer(1, 4*mm), para("SELECTED PROJECTS", "Kicker")]
projects = Table([[para("Shira Z. Carmel and her Brasserie", "CellTitle"), para("Horn-driven songs for an eight-piece ensemble", "Smallx")],[para("Infinity and One — Lullabies for Mothers", "CellTitle"), para("Hebrew motherhood-song project", "Smallx")],[para("The Hazelnuts", "CellTitle"), para("Vocal trio · founding member, songwriter and co-arranger · international touring", "Smallx")],[para("The Technicalities", "CellTitle"), para("Yiddish experimental duo", "Smallx")],[para("Shira Z. Carmel Quartet", "CellTitle"), para("Original songs across jazz, alternative pop and cabaret", "Smallx")]], colWidths=[56*mm,115*mm])
projects.setStyle(TableStyle([("VALIGN",(0,0),(-1,-1),"TOP"),("LINEBELOW",(0,0),(-1,-2),.4,colors.HexColor("#d6c8b8")),("LEFTPADDING",(0,0),(-1,-1),0),("RIGHTPADDING",(0,0),(-1,-1),3*mm),("TOPPADDING",(0,0),(-1,-1),2.4*mm),("BOTTOMPADDING",(0,0),(-1,-1),2.4*mm)]))
story += [projects, Spacer(1, 5*mm), para("MEDIA & LINKS", "Kicker")]
links = Table([
 [para("LISTEN", "Kicker"), para('<link href="https://open.spotify.com/artist/2ndGjd3SoSe42MciHjOWFA" color="#7d263d">Spotify</link>  ·  <link href="https://music.apple.com/il/artist/shira-z-carmel/1257025430" color="#7d263d">Apple Music</link>  ·  <link href="https://shiracarmel.bandcamp.com/" color="#7d263d">Bandcamp</link>  ·  <link href="https://www.youtube.com/playlist?list=PLTuSlYiHg9ANswXjZBzDSNEgvzb28MIU8" color="#7d263d">Infinity and One</link>', "Smallx")],
 [para("WATCH", "Kicker"), para('<link href="https://youtu.be/EkcrpgFOIRI" color="#7d263d">Brasserie</link>  ·  <link href="https://www.youtube.com/watch?v=RlHxK9qha18" color="#7d263d">The Hazelnuts</link>  ·  <link href="https://www.youtube.com/watch?v=Q33xsAOCp2o" color="#7d263d">Shira Z. Quartet</link>  ·  <link href="https://www.youtube.com/watch?v=RTHmF65Jvow" color="#7d263d">The Technicalities</link>', "Smallx")],
 [para("PHOTOS", "Kicker"), para("High-resolution artist portrait and official single artwork included in the online EPK, with direct downloads.", "Smallx")],
 [para("CONTACT", "Kicker"), para('<link href="mailto:contact@shiracarmel.com" color="#7d263d">contact@shiracarmel.com</link>  ·  <link href="https://www.instagram.com/shzec/" color="#7d263d">Instagram</link>  ·  <link href="https://www.facebook.com/ShZeC/" color="#7d263d">Facebook</link>  ·  <link href="https://www.youtube.com/user/shzec" color="#7d263d">YouTube</link>', "Smallx")],
 [para("MANAGEMENT", "Kicker"), para('AED Artist Management  ·  <link href="mailto:jeff@aedam.com.au" color="#7d263d">jeff@aedam.com.au</link>  ·  <link href="https://aedam.com.au/" color="#7d263d">aedam.com.au</link>', "Smallx")]
], colWidths=[30*mm,141*mm])
links.setStyle(TableStyle([("VALIGN",(0,0),(-1,-1),"TOP"),("LINEBELOW",(0,0),(-1,-1),.4,colors.HexColor("#d6c8b8")),("LEFTPADDING",(0,0),(-1,-1),0),("RIGHTPADDING",(0,0),(-1,-1),3*mm),("TOPPADDING",(0,0),(-1,-1),2.2*mm),("BOTTOMPADDING",(0,0),(-1,-1),2.2*mm)]))
story += [links]
doc.build(story, onFirstPage=frame, onLaterPages=frame)
print(OUT)
