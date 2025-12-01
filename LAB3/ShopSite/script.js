async function fetchData()
{
    let target = "https://dummyjson.com/products";
    const response = await fetch(target);

    if (!response.ok)
    {
        throw new Error(`Response status: ${response.status}`);
    }

    const jsondata = await response.json();
    return jsondata;
}


async function createPageContent() {
    
    const jsondata = await fetchData();
    const shopItems = jsondata.products;
    let mainSection = document.querySelector("main");
    
    for (let i = 0; i < 30; i++)
    {
        let item = shopItems[i];
        
        let entry = document.createElement("div");
        entry.className = "shop-item";
        
        let title = document.createElement("span");
        title.className = "title";
        title.innerHTML = item.title;
        
        let description = document.createElement("span");
        description.className = "description";
        description.innerHTML = item.description;
        
        let thumbnail = document.createElement("img");
        thumbnail.className = "thumbnail";
        thumbnail.src = item.thumbnail;
        
        entry.appendChild(title);
        entry.appendChild(description);
        entry.appendChild(thumbnail);
        
        mainSection.appendChild(entry)
    }
}

createPageContent();