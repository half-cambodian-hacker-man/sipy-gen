from sipy import Context


def build(ctx: Context):
  templating = ctx.ext("templating")
  md = ctx.ext("markdown")
  highlighting = ctx.ext("highlighting")
  minification = ctx.ext("minification")

  markdown_template = templating.from_file("build_src/markdown_template.html.j2")

  css_styles = open("build_src/styles.css").read()
  css_styles = minification.minify_css(css_styles)

  nav = {
    "Home": "/",
  }

  for name in ctx.names:
    if name.endswith(".md"):
      content = ctx.read_text(name)
      metadata, content = md.parse_frontmatter(content)
      if not "title" in metadata:
        raise NameError(f"No title for page {name}")

      rendered_markdown = md.render(content, highlighting=highlighting)

      content = markdown_template.render(
        content=rendered_markdown,
        **metadata,
        **{
          "styles": css_styles,
          "nav": nav
        }
      )

      ctx.write_text(name[:-len(".md")] + ".html", minification.minify_html(content))
    else:
      ctx.copy(name)
