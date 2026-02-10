# 📦 Instrucciones para Publicar el Juego Online

## Opción 1: GitHub Pages (Recomendado - GRATIS)

### Paso 1: Crear repositorio en GitHub
1. Ve a https://github.com y crea una cuenta si no tienes
2. Crea un nuevo repositorio (puede ser público o privado)
3. Nómbralo como quieras, por ejemplo: `juego-lucero`

### Paso 2: Subir el código
Desde la terminal de VS Code (Ctrl + `)

```bash
# Inicializar git
git init

# Agregar los archivos
git add .

# Hacer commit
git commit -m "Juego de amor para Lucero"

# Conectar con GitHub (reemplaza con tu URL)
git remote add origin https://github.com/TU_USUARIO/juego-lucero.git

# Subir
git branch -M main
git push -u origin main
```

### Paso 3: Activar GitHub Pages
1. Ve a tu repositorio en GitHub
2. Settings → Pages (en el menú izquierdo)
3. En "Source" selecciona "GitHub Actions"
4. El workflow .github/workflows/deploy.yml se ejecutará automáticamente

### Paso 4: ¡Listo!
En unos minutos tu juego estará en:
```
https://TU_USUARIO.github.io/juego-lucero
```

Copia esa URL y compártela con Lucero ❤️

---

## Opción 2: Probar Localmente Primero

Antes de subir a GitHub, puedes probar cómo se ve en web:

```bash
# Instalar pygbag
pip install pygbag

# Ejecutar en modo web
pygbag juego_amor.py
```

Se abrirá automáticamente en tu navegador. Si todo funciona bien, sube a GitHub.

---

## Opción 3: Netlify Drop (Más Rápido)

1. Ejecuta: `pygbag --build juego_amor.py`
2. Ve a https://app.netlify.com/drop
3. Arrastra la carpeta `build/web` 
4. ¡Listo! Te dará una URL instantánea

---

## 💡 Consejos

- **Privado**: Si quieres que solo Lucero lo vea, compártele la URL directamente sin publicarla en redes
- **Móvil**: El juego funciona en celulares con controles táctiles
- **Personalizar**: Puedes cambiar los colores, mensajes y cantidad de dramas en el código

---

## ❓ Problemas Comunes

**"No se ve en el celular"**
- Asegúrate de haber hecho `git push` después de los cambios
- Espera 2-3 minutos para que GitHub Pages se actualice

**"Error en GitHub Actions"**
- Ve a la pestaña "Actions" en tu repositorio
- Revisa los logs del error

**"La fuente se ve diferente"**
- Es normal, los navegadores usan fuentes web predeterminadas
