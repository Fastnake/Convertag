import flet as ft
from converti import converted
import os

async def main(page: ft.Page):
    page.title = "Convertag"
    page.horizontal_alignment=ft.CrossAxisAlignment.CENTER
    page.vertical_alignment=ft.MainAxisAlignment.CENTER
    page.window.width=700
    page.window.height=600
    page.window.resizable=False

    page.update()
    await page.window.center()

    status_text = ft.Text(size=20, weight=ft.FontWeight.BOLD, color=ft.Colors.BLUE_400, value="Нажмите на область, чтобы выбрать файл для конвертации...", text_align=ft.TextAlign.CENTER)


    # Создаем FilePicker для вызова Проводника, в скобочках было on_result=on_file_selected
    file_picker = ft.FilePicker()
    # По новым правилам сервисы обязательно регистрируются в сервисы
    page.services.append(file_picker)

    # Асинхронный триггер для безопасного запуска корутины pick_files
    async def trigger_picker(e):
        #await file_picker.pick_files(
        #allow_multiple=False 
        files_result = await file_picker.pick_files(allow_multiple=False)

        if files_result and len(files_result) > 0:
            # Мгновенно забираем путь к файлу
            selected_file_path = files_result[0].path

            page.session.store.set("file_path", selected_file_path)
            #file_path = selected_file_path

            clickable_area.visible = False
            
            preview_image.src = selected_file_path 
            preview_image.visible = True
            
            file_name_text.value = os.path.basename(selected_file_path)
            file_name_text.visible = True
            
            
            ext_button.visible = True
            status_text.value = ""
            # Меняем видимость элементов
            text.visible = True
            ext_button.visible = True
                
            status_text.value = f"Выбран файл: {os.path.basename(selected_file_path)}"
            status_text.color = ft.Colors.BLUE_400
            page.update()
        else:
            # Если пользователь нажал "Отмена"
            text.visible = False
            ext_button.visible = False
            status_text.value = "Выбор файла отменен"
            status_text.color = ft.Colors.BLUE_GREY
            page.update()
            

    clickable_area = ft.GestureDetector(
       
        mouse_cursor=ft.MouseCursor.CLICK,
        on_tap=trigger_picker, 
        
        
        content=ft.Container(
            content=ft.Column(
                [
                    ft.Icon(ft.Icons.IMAGE_SEARCH, size=60, color=ft.Colors.BLUE_400),
                    ft.Text("ВЫБРАТЬ КАРТИНКУ", size=16, weight=ft.FontWeight.W_700),
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            ),
            width=400,
            height=220,
            border=ft.Border.all(3, ft.Colors.BLUE_400),
            border_radius=20,
            bgcolor=ft.Colors.SURFACE_CONTAINER_HIGHEST,
            padding=20,
            visible=True
        )
    )

    def submit_click(e):
        extex=page.session.store.get("extex")
        file_path=page.session.store.get("file_path")
            
        converted(file_path, extex, quality=quality_slider.value)
        status_text.visible=True
        status_text.value = "Ваш файл уже конвертирован выберите ещё файлы для конвертации"
        clickable_area.visible=True
        preview_image.visible=False
        file_name_text.visible=False     
        text.visible=False
        ext_button.visible=False
        conv_button_row.visible=False
        ext_button_row.visible=False
        quality_slider.visible=False

        page.update()


    def submit_click_jpg(e):
        extex="jpg"
        page.session.store.set("extex", extex)
        quality_slider.visible=True
        conv_button_row.visible=True
        ext_button_row.visible=False
        page.update()

    def submit_click_jfif(e):
        extex="jfif"
        page.session.store.set("extex", extex)
        quality_slider.visible=True
        conv_button_row.visible=True
        ext_button_row.visible=False
        page.update()

    def to_back(e):
        quality_slider.visible=False
        conv_button_row.visible=False
        ext_button_row.visible=True

        page.update

    def submit_click_webp(e):
        extex="webp"
        page.session.store.set("extex", extex)
        quality_slider.visible=True
        conv_button_row.visible=True
        ext_button_row.visible=False
        page.update()

    def submit_click_png(e):
        extex="png"
        page.session.store.set("extex", extex)
        conv_button_row.visible=True
        ext_button_row.visible=False
        page.update()

    def submit_click_ch(e):
        ext_button_row.visible=True
        ext_button.visible=False
        page.update


    
    conv_button_row = ft.Row(
            controls=[ft.FilledButton(content="Начать",
                                      on_click=submit_click, 
                                      width=150, height=50,
                                      color=ft.Colors.BLUE_400,
                                      bgcolor=ft.Colors.BLACK,),
                      ft.FilledButton(content="Назад",
                                      on_click=to_back, 
                                      width=120, height=50,
                                      color=ft.Colors.BLUE_400,
                                      bgcolor=ft.Colors.BLACK),
                      ],
                      alignment=ft.MainAxisAlignment.CENTER,
                      visible=False
        )

    ext_button = ft.FilledButton(
        content=ft.Text("Выбрать"), 
        on_click=submit_click_ch,
        width=150,
        height=50,
        color=ft.Colors.BLUE_400,
        bgcolor=ft.Colors.BLACK,
        visible=False
        )
    
    text = ft.Text(size=14, color=ft.Colors.BLUE_400, value="Выберите в какой формат конвертировать", text_align=ft.TextAlign.CENTER, visible=False)

    ext_button_row = ft.Row(
        controls=[ft.FilledButton(content="JPG",
                                  on_click=submit_click_jpg, 
                                  width=150, height=50,
                                  color=ft.Colors.BLUE_400,
                                  bgcolor=ft.Colors.BLACK,),
                  ft.FilledButton(content="PNG",
                                  on_click=submit_click_png, 
                                  width=150, height=50,
                                  color=ft.Colors.BLUE_400,
                                  bgcolor=ft.Colors.BLACK),
                  ft.FilledButton(content="WEBP",
                                  on_click=submit_click_webp, 
                                  width=150, height=50,
                                  color=ft.Colors.BLUE_400,
                                  bgcolor=ft.Colors.BLACK),
                  ft.FilledButton(content="JFIF",
                                  on_click=submit_click_jfif, 
                                  width=150, height=50,
                                  color=ft.Colors.BLUE_400,
                                  bgcolor=ft.Colors.BLACK),
                  ],
                  alignment=ft.MainAxisAlignment.CENTER,
                  visible=False
    )


    preview_image = ft.Image(
        src="", 
        width=200, 
        height=200, 
        fit=ft.BoxFit.CONTAIN,
        visible=False  # Показываем только после выбора файла 
    )

    file_name_text = ft.Text(
        value="", 
        size=16, 
        weight=ft.FontWeight.BOLD, 
        text_align=ft.TextAlign.CENTER,
        visible=False
    )

    quality_slider = ft.Slider(
        min=0,
        max=100,
        value=90,          
        divisions=10,      
            
        label="Качество: {value}%", 
            
            
        active_color=ft.Colors.BLUE,
        thumb_color=ft.Colors.BLUE_400,
        visible=False
        )
    
    page.add(
        status_text,
        clickable_area,
        preview_image,
        file_name_text,       
        text,
        ext_button,
        ext_button_row,
        quality_slider,
        conv_button_row
    )
       

if __name__ == "__main__":
    ft.run(main)
