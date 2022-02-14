import treepoem
image = treepoem.generate_barcode(
    barcode_type="code128",  # One of the BWIPP supported codes.
    # barcode_type="qrcode",  
    # One of the BWIPP supported codes.
    # barcode_type="interleaved2of5",  # One of the BWIPP supported codes.
    # barcode_type="code128",  # One of the BWIPP supported codes.
    # barcode_type="isbn",  # One of the BWIPP supported codes.
    # data="978-3-16-148410-0",
    # barcode_type="code128",  # One of the BWIPP supported codes.
    # barcode_type="micropdf417",  # One of the BWIPP supported codes.
    # barcode_type="ean13",  # One of the BWIPP supported codes.
    data="978316148fsd4100",
    options= {"includetext": True}
)
image.convert("1").save("output_qrcode_or_barcode11.png")


import treepoem
image = treepoem.generate_barcode(
    barcode_type="code128",  # One of the BWIPP supported codes.
    data="Yout text-978316148fsd4100",
    options= {"includetext": True}
)
image.convert("1").save("output_qrcode_or_barcode.png")


import treepoem
image = treepoem.generate_barcode(
    barcode_type="code128",  # One of the BWIPP supported codes.
    data="t-18", # ekta char & - require
    options= {"includetext": True, "height":0.2, "showborder":True, "borderwidth":1, "borderbottom":8},
)
image.convert("1").save("output.png")
