fn main() {
    let contents = std::fs::read_to_string("data.txt").expect("this should work");
    let input = parse_input(contents);
    part1(input.clone());
    part2(input);
}

fn part1((crate_piles, robot_input): (Vec<Vec<char>>, String)) {
    let mut piles = crate_piles;
    // println!("{:?}", piles);

    for line in robot_input.split("\r\n") {
        let (n_crates, from, to) = get_robot_instructions(line);
        // println!("{} crates from {} to {}", n_crates, from, to);
        for _ in 0..n_crates {
            let c = piles[from].remove(0);
            piles[to].insert(0, c);
            // println!("{}: {:?}", i, piles)
        }
    }
    let mut top = String::new();
    for i in 0..piles.len() {
        let pile = piles[i].clone();
        top += &pile[0].to_string();
    }
    println!("Part1: {}", top);
}

fn part2((crate_piles, robot_input): (Vec<Vec<char>>, String)) {
    let mut piles = crate_piles.clone();
    for line in robot_input.split("\r\n") {
        let (n_crates, from, to) = get_robot_instructions(line);

        let (c, mut new_pile) = piles[from].split_at(n_crates);
        
        let mut cv = c.to_vec();
        cv.extend(piles[to].clone());

        let mut new_from_vec = new_pile.to_owned().to_vec();
        piles[from] = new_from_vec;

        piles[to] = cv;


    }
    let mut top = String::new();
    for i in 0..piles.len() {
        let pile = piles[i].clone();
        top += &pile[0].to_string();
    }
    println!("Part2: {}", top);
}

fn get_robot_instructions(line: &str) -> (usize, usize, usize) {
    let n_crates = line.split("from").collect::<Vec<&str>>()[0]
        .split_at(4)
        .1
        .trim()
        .parse::<usize>()
        .unwrap();
    let from = line.split("from").collect::<Vec<&str>>()[1]
        .split("to")
        .collect::<Vec<&str>>()[0]
        .trim()
        .parse::<usize>()
        .unwrap()
        - 1;
    let to = line.split("from").collect::<Vec<&str>>()[1]
        .split("to")
        .collect::<Vec<&str>>()[1]
        .trim()
        .parse::<usize>()
        .unwrap()
        - 1;
    (n_crates, from, to)
}

fn parse_input(input: String) -> (Vec<Vec<char>>, String) {
    // fn parse_input(input : String) {
    // println!("{:?}", input);
    let mut crates_input = input.split("\r\n\r\n").collect::<Vec<&str>>()[0];
    // println!("Crates: {:?}", crates_input);
    let crates = crates_input.split("\r\n").collect::<Vec<&str>>();
    let last = crates.last().unwrap();
    let cols: u32 = last.split_at(last.len() - 4).1.trim().parse().unwrap();
    let mut crate_rows = crates_input.split("\r\n").collect::<Vec<&str>>();
    crate_rows.pop();
    let mut crate_piles: Vec<Vec<char>> = vec![Vec::new(); cols as usize];
    for row in crate_rows {
        // println!("Row: {:?}", row);
        // println!("Cols: {:?}", cols);
        for i in 0..(cols) {
            let c = get_crate_at_col(row, i as usize);
            // println!("Crate at {}: {:?}",i, c);
            if c.is_some() {
                crate_piles[i as usize].push(c.unwrap());
            }
        }
    }
    // let mut robot_input = input.split("\r\n\r\n").collect::<Vec<&str>>()[1].split("\r\n").collect::<Vec<&str>>();
    let robot_input = input.split("\r\n\r\n").collect::<Vec<&str>>()[1].to_string();
    // println!("Robots: {:?}", robot_input);
    // println!("Crate Piles: {:?}", crate_piles);
    (crate_piles, robot_input)
}

fn get_crate_at_col(input: &str, column: usize) -> Option<char> {
    let c = input
        .split_at(((column + 1) * 4) - 1)
        .0
        .split_at(4 * column)
        .1;
    if c.trim() == "" {
        None
    } else {
        Some(c.chars().nth(1).unwrap())
    }
}
