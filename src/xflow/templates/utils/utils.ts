export function createCumulativeStartEndRangesFromValues(array: number[], base_value: number): [number, number][] {
  let cumulative = 0;
  return array.map((value, index) => {
    if (index === 0) {
      cumulative = base_value;
    }
    const start = cumulative;
    cumulative += value;
    return [start, cumulative];
  });
}