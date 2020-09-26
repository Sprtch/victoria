{% set barcode_length = number | length -%}
{% set name_length = name | length -%}
{% set title_height = 45 -%}
{% set title_line = 4 -%}
{% set title_margin = 5 -%}
{% set width = 70 -%}
{% set height = 50 -%}
{% set dpmm = 12 -%}
{% set logo_width = 42 -%}
{% set logo_offset = 36 -%}
{% set barcode_height = 120 -%}
{% set barcode_size = 2 -%}
{% set barcode_font = 30 -%}
^XA

^FX SEPARTECH LOGO SECTION

^FO{{ ((width * dpmm) - (logo_width * dpmm)) // 2 }},{{ logo_offset * dpmm }}^GFA,2032,2032,16,,:I01FE,I07FFC,001IFE,003JF8K07FC,007JFCJ01IF,00KFCJ03IF8K07,01KFEJ07IFCJ03FE,01LFJ0JFEJ07FF,03LFJ0KFJ0IF8,03LFI01KFI01IFC,03LF8001KFI01IFC,07LF8001KF8001IFE,07LF8001KF8003IFE,07LF8003KF8003IFE,07LF8001KF8003IFE,:03LF8001KF8001IFE,03LF8001KFI01IFC,03LFJ0KFJ0IFC,01LFJ0JFEJ07FF8,01KFEJ07IFEJ03FF,00KFEJ03IFCJ01FC,00KFCJ01IF8,007JF8K0FFE,003JFL01F8,I0IFE,I03FF8,J07C,,:::::I01FF,I0IFC,001JFM06,003JF8K07FC,007JFCJ01IF,00KFEJ03IF8K078,01KFEJ07IFCJ03FE,01LFJ0JFEJ07FF,03LFJ0KFJ0IF8J0F8,03LF8001KFI01IFCI03FC,03LF8001KFI01IFCI07FE,07LF8001KF8001IFEI07FE,07LF8001KF8003IFEI07FE,07LF8003KF8003IFEI0FFE,07LF8001KF8003IFEI07FE,:03LF8001KF8001IFEI07FE,03LF8001KFI01IFCI03FC,03LFJ0KFJ0IFCI01F8,01LFJ0JFEJ07FF8,01KFEJ07IFEJ03FF,00KFEJ03IFCK0FC,00KFCJ01IF8,007JF8K0FFE,003JFL01F,I0IFE,I03FF8,J078,,:::::I01FF,I0IFC,001JFM0E,003JF8K07FE,007JFCJ01IF,00KFEJ03IF8K0F8,01KFEJ07IFCJ03FE,01LFJ0JFEJ07FF8,03LFJ0KFJ0IF8J0F8,03LF8001KFI01IFCI03FC,03LF8001KFI01IFEI07FE,07LF8001KF8001IFEI07FE,07LF8001KF8003IFEI07FE,07LF8003KF8003IFEI0FFE,07LF8001KF8003IFEI07FE,:03LF8001KFI01IFEI07FE,03LF8001KFI01IFCI03FC,03LFJ0KFJ0IFCI01F8,01LFJ0JFEJ07FF8,01KFEJ07IFEJ03FF,00KFEJ03IFCK0F8,007JFCJ01IF,007JF8K0FFE,001JFL01F,I0IFC,I03FF,J03,,:::::::T0F,S07FC,S0FFE,R01IFL0F8,R03IF8J01FC,R03IFCJ03FE,R03IFCJ07FF,R07IFCJ07FF,:::R03IFCJ03FF,R03IF8J03FE,R01IF8K0FC,S0IF,S07FE,S03F8,,:::^FS

^FO{{ (((width * dpmm) - (logo_width * dpmm)) // 2) + (12 * dpmm) }},{{ logo_offset * dpmm + 4 * dpmm }}^GFA,3082,3082,46,,:::::J0IFiN0C,I07IFEI01MF007JFEL03FFK01KF8I0NFE00LF8J03FFEI01EL07,001KF8001MF007KFCK03FF8J01LFI0NFE01LF8J0JFC001EL0F,007KFC001MF007LFK03FF8J01LFE00NFE01LF8I03JFE001EL0F,00MF001LFE007LF8J07FF8J01MF00NFE01LF8I07F007F801EL0F,01MF801LFE007LFEJ07FFCJ01MF8J01EK01EN01FCI0F801EL0F,01FFC03FF801LFE007MFJ07FFCJ01MFCJ01EK01EN03FJ07801EL0F,03FFI0FF001FEM07FI07FFJ07FFCJ01FEI0FFEJ01EK01EN03EJ01001EL0F,03FCI03E001FEM07FI01FF8I0FEFCJ01FEI03FFJ01EK01EN07CM01EL0F,07F8J0C001FEM07FJ0FFCI0FEFEJ01FEI01FFJ01EK01EN0F8M01EL0F,07F8M01FEM07FJ07FCI0FCFEJ01FEJ0FFJ01EK01EM01FN01EL0F,07F8M01FEM07FJ03FC001FCFEJ01FEJ0FF8I01EK01EM01EN01EL0F,07FN01FEM07FJ03FE001FC7FJ01FEJ07F8I01EK01EM03EN01EL0F,07FN01FEM07FJ01FE001F87FJ01FEJ07F8I01EK01EM03CN01EL0F,07FN01FEM07FJ01FE003F87FJ01FEJ07F8I01EK01EM03CN01EL0F,07F8M01FEM07FJ01FE003F83F8I01FEJ07F8I01EK01EM07CN01EL0F,07F8M01FEM07FJ01FE003F03F8I01FEJ07F8I01EK01EM078N01EL0F,07FCM01FEM07FJ01FE007F03F8I01FEJ07F8I01EK01EM078N01EL0F,03FEM01FEM07FJ01FE007F01FCI01FEJ07F8I01EK01EM078N01EL0F,03FFM01FEM07FJ01FE007F01FCI01FEJ07F8I01EK01EM0F8N01EL0F,03FFCL01FEM07FJ01FE00FE01FCI01FEJ0FFJ01EK01EM0FO01EL0F,01IF8K01FEM07FJ01FE00FE01FEI01FEI01FFJ01EK01EM0FO01EL0F,00JFK01FEM07FJ03FC00FE00FEI01FEI01FFJ01EK01EM0FO01EL0F,007IFEJ01LFI07FJ03FC01FC00FEI01FEI07FEJ01EK01EM0FO01EL0F,001JF8I01LF8007FJ07FC01FC00FFI01FE001FFCJ01EK01KFC00FO01NF,I0KFI01LF8007FJ0FF801FC007FI01MF8J01EK01KFC00FO01NF,I03JF8001LF8007FI03FF803F8007FI01MFK01EK01KFC00FO01NF,J07IFC001LF8007F001IF003F8007F8001LFEK01EK01KFC00FO01NF,K0JF001LF8007LFE003F8007F8001LF8K01EK01EM0FO01EL0F,K01IF001LFI07LFC007F8003F8001KFCL01EK01EM0FO01EL0F,L07FF801FEM07LFI07FI03FC001KFCL01EK01EM0FO01EL0F,L01FFC01FEM07KFEI07FI03FC001FE01FEL01EK01EM0FO01EL0F,M07FC01FEM07KFJ07F0301FC001FE01FFL01EK01EM0FO01EL0F,M03FC01FEM07JFK0FE0FC1FC001FE00FFL01EK01EM0FO01EL0F,M03FE01FEM07FN0FE1FF1FE001FE007F8K01EK01EM0FO01EL0F,M01FE01FEM07FN0FE3FF0FE001FE007FCK01EK01EM0F8N01EL0F,M01FE01FEM07FM01FC3FF8FE001FE003FCK01EK01EM078N01EL0F,M01FE01FEM07FM01FC3FF8FF001FE003FEK01EK01EM078N01EL0F,M01FE01FEM07FM01FC7FF8FF001FE001FEK01EK01EM078N01EL0F,M01FE01FEM07FM03FC3FF87F001FE001FFK01EK01EM03CN01EL0F,M01FE01FEM07FM03F83FF07F801FEI0FF8J01EK01EM03CN01EL0F,M01FE01FEM07FM03F81FF07F801FEI07F8J01EK01EM03EN01EL0F,M03FE01FEM07FM07F80FE03F801FEI07FCJ01EK01EM01EN01EL0F,03K03FC01FEM07FM07F007803FC01FEI03FCJ01EK01EM01FN01EL0F,07CJ07FC01FEM07FM07FK03FC01FEI03FEJ01EK01EN0F8M01EL0F,0FEJ0FF801FEM07FM0FFK01FC01FEI01FFJ01EK01EN0F8M01EL0F,1FFC003FF801FEM07FM0FEK01FE01FEI01FFJ01EK01EN07CJ01001EL0F,1IFC3IF001MF807FM0FEK01FE01FEJ0FF8I01EK01EN03FJ03801EL0F,0MFE001MF807FL01FEK01FE01FEJ0FF8I01EK01EN01F8I0FC01EL0F,07LFC001MF807FL01FEL0FF01FEJ07FCI01EK01EO0FE003F801EL0F,01LF8001MF807FL01FCL0FF01FEJ03FEI01EK01LFCI07KF001EL0F,007JFEI01MF807FL03FCL0FF01FEJ03FEI01EK01LFCI01JFE001EL0F,I0JF8I01MF807FL03FCL07F81FEJ01FFI01EK01LFCJ07IF8001EL0F,I01FF8iM0FF8,,::::::^FS

^FX Product title

^CFE,{{ title_height }}^FO{{ title_margin * dpmm }},{{ title_height }}
^FB{{ (width * dpmm) - (title_margin * dpmm) }},{{ title_line }},3,C^FH
^FD{{ name }}^FS

^FX BARCORDE SECTION.

^FO{{ ((width * dpmm) - (11 * barcode_size * barcode_length + 11 * barcode_size + 11 * barcode_size + 12 * barcode_size)) // 2 }},{{ 50 + title_line * title_height }}^BY{{ barcode_size }}
^BCN,{{ barcode_height }},N,N,N
^FD{{ number }}^FS

^CFA,{{ barcode_font }}^FO0,{{ 60 + title_line * title_height + barcode_height }}
^FB{{ width * dpmm }},{{ title_line }},1,C^FH
^FD{{ number }}^FS

^XZ
