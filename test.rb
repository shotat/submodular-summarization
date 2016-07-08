require './lib/doc_submodular.rb'

texts = []
begin
  File.open('sample.txt') do |file|
    file.each_line do |line|
      texts << line
    end
  end
  # 例外は小さい単位で捕捉する
rescue SystemCallError => e
  puts %Q(class=[#{e.class}] message=[#{e.message}])
rescue IOError => e
  puts %Q(class=[#{e.class}] message=[#{e.message}])
end

doc_costs = DocCosts.new(texts);
sample_vec = doc_costs.zero_vec
sample_vec[0] = 1
sample_vec[1] = 1
sample_vec[6] = 1
puts doc_costs.relevance(sample_vec, 0.2)
