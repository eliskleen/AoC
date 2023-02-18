// use dict::Dict;
use num_derive::FromPrimitive;
use num_derive::ToPrimitive;
use num_traits::FromPrimitive;
use num_traits::ToPrimitive;
use std::collections::HashMap;
#[derive(Eq, Hash, PartialEq, Clone, FromPrimitive, ToPrimitive)]
enum RPS {
    Rock = 0,
    Paper = 1,
    Scissors = 2,
} // + 1 => win , -1 => lose, 0 => tie

fn main() {
    let contents = std::fs::read_to_string("data.txt").expect("this should work");
    let input = parse_input1(contents.clone());
    part1(input);
    let i2 = parse_input2(contents);
    part1(i2);
}

fn part1(input: Vec<(RPS, RPS)>) {
    let mut score: HashMap<RPS, u32> = HashMap::new();
    score.insert(RPS::Rock, 1);
    score.insert(RPS::Paper, 2);
    score.insert(RPS::Scissors, 3);
    let mut game: HashMap<(RPS, RPS), u32> = HashMap::new();
    game.insert((RPS::Rock, RPS::Scissors), 6);
    game.insert((RPS::Scissors, RPS::Paper), 6);
    game.insert((RPS::Paper, RPS::Rock), 6);
    game.insert((RPS::Rock, RPS::Paper), 0);
    game.insert((RPS::Scissors, RPS::Rock), 0);
    game.insert((RPS::Paper, RPS::Scissors), 0);
    game.insert((RPS::Rock, RPS::Rock), 3);
    game.insert((RPS::Scissors, RPS::Scissors), 3);
    game.insert((RPS::Paper, RPS::Paper), 3);
    let mut total_score = 0;
    for (me, op) in input {
        total_score += get_game_score(me, op, &game, &score);
    }
    println!("total score: {}", total_score);
}
fn get_game_score(
    me: RPS,
    op: RPS,
    game: &HashMap<(RPS, RPS), u32>,
    score: &HashMap<RPS, u32>,
) -> u32 {
    let game_score = game.get(&(me.clone(), op)).unwrap();
    let my_score = score.get(&me).unwrap();
    game_score + my_score
}
fn parse_input2(input: String) -> Vec<(RPS, RPS)> {
    let m = |s| match s {
        "A" => RPS::Rock,
        "B" => RPS::Paper,
        "C" => RPS::Scissors,
        _ => panic!("Invalid input"),
    };

    let me = |o: RPS, s| {
        let op = ToPrimitive::to_i32(&o).unwrap();
        let mut m = match s {
            "X" => (op - 1) % 3,
            "Y" => op,
            "Z" => (op + 1) % 3,
            _ => panic!("Invalid input"),
        };
        m = if m < 0 { m + 3 } else { m };
        FromPrimitive::from_i32(m).unwrap()
    };
    input
        .lines()
        .map(|line| {
            let split = line.split_whitespace().collect::<Vec<&str>>();
            let o = m(split[0]);
            let m = me(o.clone(), split[1]);
            (m, (o))
        })
        .collect()
}
fn parse_input1(input: String) -> Vec<(RPS, RPS)> {
    // println!("input: {}", input);
    return input.lines().map(to_rps).collect();
}
fn to_rps(pair: &str) -> (RPS, RPS) {
    let m = |s| match s {
        "A" => RPS::Rock,
        "B" => RPS::Paper,
        "C" => RPS::Scissors,
        "X" => RPS::Rock,
        "Y" => RPS::Paper,
        "Z" => RPS::Scissors,
        _ => panic!("Invalid input"),
    };
    let split = pair.split_whitespace().collect::<Vec<&str>>();
    (m(split[1]), m(split[0]))
}
