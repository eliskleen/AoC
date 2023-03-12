fn main() {
    let contents = std::fs::read_to_string("data.txt")
                        .expect("this should work");
    let input = parse_input(contents);
    part1(input.clone());
    part2(input);

}



fn part1(input : Vec<Vec<u32>>) {
    let mut score = 0;
    for sac in input {
        let mid_index = sac.len() / 2;
        let (c1, c2) = sac.split_at(mid_index);
        let t = c1.iter().find(|i| c2.contains(i)).unwrap();
        // println!("{}", t);
        score += t;
    }
    println!("Part 1: {}", score);
}

fn part2(input: Vec<Vec<u32>>){
    let mut score = 0;
    for group in input.chunks(3) {
        let (c1, c2, c3) = (group[0].clone(), group[1].clone(), group[2].clone());
        let mut t = c1.iter().find(|i| c2.contains(i) && c3.contains(i)).unwrap();
        score += t;
    }
    println!("Part 2: {}", score);
}

fn parse_input(input : String) ->  Vec<Vec<u32>>{
    let mut result = Vec::new();
    let prio = |ch:char| match ch.is_lowercase() {
        true => ch as u32 - 96,
        false => ch as u32 - 64 + 26
    };
    for line in input.lines() {
        let mut l : Vec<u32> = line.chars().map(|c| prio(c)).collect();
        result.push(l);
    }
    result
}

