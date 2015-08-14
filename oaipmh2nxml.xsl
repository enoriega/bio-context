<xsl:stylesheet
  version="1.0"
  xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
  xmlns:nxml="http://dtd.nlm.nih.gov/2.0/xsd/archivearticle"
  xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
  xsi:schemaLocation="http://dtd.nlm.nih.gov/archiving/2.3/xsd/archivearticle.xsd"
>
  <xsl:output indent="yes" />

  <!-- Select any subtree with a "Person" element as the root -->
   <xsl:template match="/">
          <xsl:apply-templates select="descendant::nxml:article" />
   </xsl:template>
   <!-- Copy everything that has been selected -->
   <xsl:template match="@*|*|text()" >
      <xsl:copy>
         <xsl:apply-templates select="@*|*|text()" />
      </xsl:copy>
   </xsl:template>
</xsl:stylesheet>
