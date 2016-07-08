require './lib/doc_submodular.rb'

texts = []
begin
  File.open('recruit.txt') do |file|
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


def greedy_search(k, texts)
  params = { gumma: 0.5 }
  doc_submodular = DocSubmodular.new(texts, params);
  # step 0
  s = []
  s_ = []
  # step 1
  while k > doc_submodular.cost_sum(s)
    # step  2
    s_ = s
    # step 3
    tmp_max = 0
    idx_max = -1
    doc_submodular.len.times do |i|
      next if s.include? i
      tmp = doc_submodular.calculate(s + [i]) / doc_submodular.cost(i)
      if tmp > tmp_max
        puts "#{tmp} #{texts[i]}"
        tmp_max = tmp
        idx_max = i
      end
    end
    s << idx_max
  end
  s_
end

result = greedy_search(140, texts)
result.each do |idx|
  puts texts[idx]
end


