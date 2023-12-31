

export default function ({articleList}){

    return articleList.map(article => <div id={article.id}>{article.id} </div>)


}