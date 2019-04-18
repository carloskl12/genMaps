# Genera Mapas (genMaps)
El presente programa permite generar mapas utilizando el concepto de ruido de perlin.

### Contenido
**[Requisitos](#requisitos)**<br>
**[Interfaz](#interfaz)**<br>
**[Origen](#origen)**<br>
**[Algunos mapas](#algunos-mapas)**<br>
**[Trabajos Futuros](#trabajos-futuros)**<br>

## Requisitos
El programa está desarrollado utilizando python 3.7.3
* wxpython: 4.0.4

## Interfaz
Consta básicamente de los parámetros:
* Semilla: valor que se utiliza para generar los valores seudoaleatorios que se usan en la generación de los relieves
* Octavas: cantidad de escalas sobre las cuales generar detalles
* Mapa periódico: Si se desea que el mapa generado coincida en sus extremos opuestos, es decir, arriba y abajo, derecha e izquierda. En otras palabras, si es periódico, se puede generar un patron continuo de azulejos.

Con el botón refrescar se genera el mapa a partir de los parámetros dados.

![interfaz](https://github.com/carloskl12/genMaps/blob/master/imagenes/interfaz.png)

## Origen
Este proyecto surgió por la inquietud de generar mapas de mundos completos. Los mapas son fuente de inspiración para posibles mundos en juegos o historias, rutinas con las cuales estimulo mi creatividad con frecuencia. Hace ya algún tiempo que quería desarrollar algo por el estilo, hasta que por fin me puse en esta tarea, para ello fué bastante inspirador un blog sobre el [ruido de perlin](https://www.lanshor.com/ruido-perlin/), mis agradecimientos a su autor  [LaNsHoR](https://github.com/LaNsHoR).

## Algunos mapas
Semilla 7:
* ![](https://github.com/carloskl12/genMaps/blob/master/imagenes/semilla7.png)

Semilla 13:
* ![](https://github.com/carloskl12/genMaps/blob/master/imagenes/semilla13.png)

Semilla 33:
* ![](https://github.com/carloskl12/genMaps/blob/master/imagenes/semilla33.png)

Semilla 51:
* ![](https://github.com/carloskl12/genMaps/blob/master/imagenes/semilla51.png)

## Trabajos futuros
Si la inspiración y los tiempos coinciden, espero que a futuro:
* Generar grillas utilizando funciones de distribución de probabilidad variadas
* Crear filtros par mejorar los relieves
* Crear la superficie sobre un planeta
* Guardar relieves del mapa
