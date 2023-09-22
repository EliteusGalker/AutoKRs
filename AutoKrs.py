import os
import asyncio
from pyppeteer import launch
import time
import sys





async def main(KRS):
    # Get the current working directory
    cwd = os.getcwd()
    
    # Specify the relative path to the Chromium executable
    chromium_path = os.path.join(cwd, 'chrome-win', 'chrome.exe')

    download_folder = os.path.join(cwd, 'downloaded_files')
    
    # Configure launch options to use the specified Chromium executable
    browser = await launch(executablePath=chromium_path, headless=False)
    
    page = await browser.newPage()

    await page.goto('https://ekrs.ms.gov.pl/krsrdf/krs/wyszukiwaniepodmiotu?.')

    #ZAZNACZ PRZEDSIĘBIORCY
    checkbox = await page.querySelector('html body div#main div.content_half form#form div#form_main div#form_body div.form_row input#rejestrPrzedsiebiorcy')
    
    if checkbox:
        # Check if the checkbox is not already checked
        is_checked = await page.evaluate('(checkbox) => checkbox.checked', checkbox)
        
        if not is_checked:
            # Click the checkbox to check it
            await checkbox.click()
            print("Checkbox clicked")
        else:
            print("Checkbox is already checked")
    else:
        print("Checkbox not found")

    #WPISZ KRS
    krs_input = await page.querySelector('html body div#main div.content_half form#form div#form_main div#form_body div.form_row div#formLeftDiv.form_left div#rowKrs.form_row div.input_main input#krs')
    if krs_input:
        await krs_input.type(KRS)
        print(f'Inserted {KRS} into the input field for KRS')
    else:
        print("KRS input field not found")

    
    #SZUKAJ
    szukaj = await page.querySelector('html body div#main div.content_half form#form div#form_main div#form_body div.form_row div input#szukaj')
    
    if szukaj:
        # Click the "Szukaj" button and wait for navigation to complete
        await asyncio.gather(
            szukaj.click(),
            page.waitForNavigation()  # Wait for the navigation to complete
        )
    else:
        print("Szukaj not found")



    

    view = await page.querySelector('html body div#main div.content_half form#form div#form_main div#form_body div#podmiotyGrid div.t-data-grid table.table tbody tr.t-first.t-last td.daneSzczegolowe a')

        
    if view:
        await view.click()
        await page.waitForNavigation()
        print("wyświetl clicked")             
    else:
        print("Szukaj not found")
        current_directory = os.path.dirname(sys.executable) if getattr(sys, 'frozen', False) else os.path.dirname(os.path.abspath(__file__))
        file_path = os.path.join(current_directory, 'downloaded_files', f"{KRS}.txt")
        try:
            # Open the file for writing
            with open(file_path, 'w') as file:
                # Write the content to the file
                content = f'Nie udało się pobrać {KRS}'
                file.write(content)
            
            print(f"File '{KRS}.txt' saved successfully in {current_directory}")
        except Exception as e:
            print(f"An error occurred while saving the file: {e}")
           


    try:

        

        # Click the button that triggers the file download
        download_button = await page.querySelector('html body div#main div.content_half div#form_main div div#form_body div form#noSubmit input#pobierzWydrukAktualny')
        if download_button:
            await download_button.click()
            print("Clicked the download button")

        # Wait for the 'download' event to be triggered

        

    except Exception as e:
        print(f"An error occurred: {e}")
    



    # Print the web content

    
    

    time.sleep(2) # zaczkeaj aż pobierze
    await browser.close()

if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(main())
