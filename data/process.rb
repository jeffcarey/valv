require 'json'
langs = Dir.entries(".").select{|s| s.end_with? ".json"}.map{|s| JSON.parse(File.read(s))}
langs.each do |lang|
  total = 0.0
  count = 0.0
  lang["categories"].each do |cat|
    cat["subcategories"].each do |subcat|
      subcat["articles"].each do |art|
        count += 1
        total += art["quality"]
      end
    end
  end
  lang["average_quality"] = total/count
end

langs = langs.sort_by{|lang| -lang["average_quality"]}

puts JSON.fast_generate(langs)
