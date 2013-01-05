ypassbook - an Apple Passbook pass generator

Usage

1. Learn required infomation from [Apple](https://developer.apple.com/passbook/)

2. In your Keychain Access, export your Pass certificate into .p12 file (like pass.com.your.cert.p12), and Apple Worldwide Developer Relations certificate into .pem file (like AppleWWDR.pem)

3. Convert your p12 files into PEMs:
    openssl pkcs12 -in "pass.com.your.cert.p12" -clcerts -nokeys -out "pass.com.your.cert.pem"
    openssl pkcs12 -in "pass.com.your.cert.p12" -nocerts -out "pass.com.your.key.pem"

4. Create your pass object and save it into a .pkpass file.
    p = Pass(Pass.EVENTTICKET, description, organizationName, passTypeId, teamId, serialNumber)
    f = Field(key, value, label)
    p.addPrimaryField(f)
    p.setLocalizedString(locale, label, labelValue)

    imagename = "icon.png" #must have an icon, and must be icon.png
    p.setImage(imagename, imagedata)

    p.logoText = "Your logo text"

    p.addLocation(latitude, longitude, altitude, name)

    p.setBarcode(Pass.PKBARCODE_FORMAT_QR, Pass.BARCODE_ENCODING_ISO_8859_1, value, text)

    # you can use p.savePackage() to save a Pass directory

    zipdata = p.getSignedPass(wwdr_data, cert_data, key_data, Passphrase)
    
    open("test.pkpass", "wb").write(zipdata) #save your pkpass file or send the data to your client


    see https://github.com/sprhawk/Passbook for more information
