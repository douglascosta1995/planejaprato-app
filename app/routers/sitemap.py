from fastapi import APIRouter
from fastapi.responses import Response

router = APIRouter()


@router.get("/sitemap.xml", include_in_schema=False)
def sitemap():
    xml = """<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">

    <url>
        <loc>https://planejaprato.onrender.com/</loc>
        <priority>1.0</priority>
    </url>

    <url>
        <loc>https://planejaprato.onrender.com/register</loc>
        <priority>0.8</priority>
    </url>

</urlset>
"""

    return Response(
        content=xml,
        media_type="application/xml"
    )
