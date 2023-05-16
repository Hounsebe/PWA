// Fonction pour créer l'élément HTML d'un objet Feed
function createFeedElement(feed) {
  const element = document.createElement("div");
  element.classList.add("element");
  element.innerHTML = `
         <div class="post-header">
           <img src="${feed.profil}" />
           <div class="end">${feed.username}</div>
         </div>
         <div class="divider"></div>
         <div class="post-body">
           <p class="post-text">${feed.text}</p>
           <img src="${feed.image}" class="post-image" />
         </div>
         <div class="post-footer">
           <div class="like">LIKE ${feed.likes}</div>
         </div>
       `;
  return element;
}

// Fonction pour effectuer le rendu des objets Feed dans le DOM
export function render(feeds) {
  const container = document.getElementById("main");
  //   container.innerHTML = "";

  feeds.forEach((feed) => {
    const element = createFeedElement(feed);
    container.appendChild(element);
  });
}
