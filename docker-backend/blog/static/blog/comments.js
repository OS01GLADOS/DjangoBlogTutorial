
URL = ''

function setUrl(value){
    URL = value
}

let last_update_date = new Date()


        function send_comments_update_request() {
            console.log(URL)
            $.get(URL, {time: last_update_date.toISOString()}, parse_comments_update_response)
        }

function parse_comments_update_response(data, success, request) {
            

            
            let res = JSON.parse(data)

            date = request.getResponseHeader('Date')

            last_update_date = new Date(date)

            if (res.length >= 1) {
                for (i = 0; i < res.length; i++) {
                    let obj_to_insert = document.createElement('div')
                    obj_to_insert.classList.add('container')

                    let img = document.createElement('img')
                    img.classList.add('rounded-circle', 'article-img')

                    let div = document.createElement('div')
                    div.classList.add('media-body')

                    let inner_div = document.createElement('div')
                    inner_div.classList.add('article-metadata')

                    let small = document.createElement('small')
                    small.classList.add('text-muted')

                    let a = document.createElement('a')
                    a.classList.add('me-2')

                    let p = document.createElement('p')
                    p.classList.add('article-content')


                    inner_div.append(a, small)
                    div.append(inner_div, p)
                    obj_to_insert.append(img, div)

                    img.src = res[i].sender_pic
                    a.href = res[i].sender_link
                    a.append(res[i].sender__username)
                    small.append(res[i].date_posted)
                    p.append(res[i].content)

                    let comments_section = $("#comments")

                    comments_section_childs = comments_section.children()
                    comments_section.innerHTML = ''
                    comments_section.append(obj_to_insert)
                    comments_section.append(comments_section_childs)

                }
            }

        }

        setInterval(send_comments_update_request, 5000);