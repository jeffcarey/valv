require 'json'

def id
  $id += 1
  $id
end

def article(min_quality, max_quality)
  { quality: rand(min_quality..max_quality), id: id}
end

def data(name:, code:, min_quality:, max_quality:)
  $id = 0
  {
    language: {name: name, code: code},
    categories: [
      {name: "People",
       subcategories: [
         {name: "Politicians", articles: 240.times.map{article min_quality, max_quality}},
         {name: "Scientists", articles: 260.times.map{article min_quality, max_quality}}
      ]},
      {name: "Things",
       subcategories: [
         {name: "Materials", articles: 100.times.map{article min_quality, max_quality}},
         {name: "Electronics", articles: 150.times.map{article min_quality, max_quality}}
      ]},
      {name: "History",
       subcategories: [
         {name: "Ancient", articles: 50.times.map{article min_quality, max_quality}},
         {name: "Classical", articles: 80.times.map{article min_quality, max_quality}},
         {name: "Modern", articles: 120.times.map{article min_quality, max_quality}},
      ]},
    ]
  }
end

languages = [
  {name: "English", code: "en", min_quality: 0.8, max_quality: 1},
  {name: "French", code: "fr", min_quality: 0.6, max_quality: 0.98},
  {name: "Swahili", code: "sw", min_quality: 0, max_quality: 0.7}
]
puts JSON.pretty_generate(languages.map{|lang| data(**lang)})
