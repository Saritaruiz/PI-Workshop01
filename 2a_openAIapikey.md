# 🔑 Creación y Protección de la API Key de OpenAI

## 📥 Paso 1: Crear tu API Key en OpenAI

1. Ingresa a la página de OpenAI: [https://openai.com/api/](https://openai.com/api/) e inicia sesión.
   
   <div align="center">
     <img src="imgs/key1.png" alt="Acceder a OpenAI">
   </div>

2. En el panel principal, haz clic en **`Dashboard`**.

   <div align="center">
     <img src="imgs/key2.png" alt="Dashboard">
   </div>

3. Haz clic en **`Create new secret key`**.

   <div align="center">
     <img src="imgs/key3.png" alt="Crear nueva llave">
   </div>

4. Asigna un nombre a tu API Key, por ejemplo: **`workshop3`**.

  <div align="center">
     <img src="imgs/key4.png" alt="Nombrar la API key">
   </div>

5. Copia la API Key generada y haz clic en **`Done`**.

   ⚠️ **Importante:** Después de cerrar esta ventana, no podrás volver a ver esta llave. Guarda la clave en un lugar seguro.

   <div align="center">
     <img src="imgs/key5.png" alt="Guardar API key">
   </div>

---

## 📥 Paso 2: Almacenar la API Key en un archivo `.env` (Protección de la clave)

Crea un archivo llamado **`openAI.env`** en la raíz del proyecto usando cualquier editor de texto (VSCode, Sublime, etc.):

```
openai_apikey="sk-XXXXXXXXXXXXXXXXXXXX"
```

<div align="center">
  <img src="imgs/key22.png" alt="Archivo env">
</div>

Ubica el archivo **`openAI.env`** en la carpeta raíz de tu proyecto:

<div align="center">
  <img src="imgs/key7.png" alt="Ubicación del archivo env">
</div>

---

## 🚨 Paso 3: ¡Protege tu API Key con `.gitignore`! 🚨

### 🔒 ¿Por qué es importante?
El archivo `.gitignore` evita que archivos sensibles (como tus llaves de API) se suban al repositorio de GitHub.

- Si tu API key llega a GitHub, puede ser detectada y **bloquearán tu push o podrán usar tu cuenta**.

### ✅ Instrucciones:
1. Verifica que el archivo **`.gitignore`** exista en la raíz de tu proyecto.
   ```bash
   echo. > .gitignore
   ```

2. Abre `.gitignore` y agrega lo siguiente al final:
```
openAI.env
*.env
.env
```

<div align="center">
  <img src="imgs/key_gitignore.png" alt="Contenido del gitignore">
</div>

✅ Así te aseguras de que la API key **NO SE SUBA** nunca al repositorio.

---

## 📌 Resultado
- Tu API key está guardada de forma segura.
- Puedes cargar la clave desde el archivo `.env` en tu código.
- Git ignorará el archivo y protegerás tus credenciales.

