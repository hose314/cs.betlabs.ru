import data from '../../db/results.json';

const LabCardTemplate = (labN, result) => {
  let
      score = result.scores.reduce((res, curr) => res += curr),
      accepted = score >= 60,
      color = accepted ? 'green' : 'red';

  const row = (i, score) => `<tr><td>${i}</td><td>${score}</td></tr>`;

  return `<div class="ui segment">
            <h4>Лабораторная работа #${labN}</h4>
            <table class="ui celled large inverted ${color} table">
                <thead>
                    <th>№ Вопроса</th>
                    <th>Score</th>
                </thead>
                <tbody>
                    ${result.scores.reduce((res, curr, i) => res += row(i + 1, curr), '')}
                </tbody>
                <tfoot>
                    <tr>
                        <th>Лабораторная работа: <strong>${accepted ? 'ПРИНЯТА': 'НЕ ПРИНЯТА'}</strong></th>
                        ${accepted ? `<th>Итог: ${score}</th>`:'<th>Причина: Недостаточно баллов или плагиат</th>'}
                    </tr>
                </tfoot>
            </table>
        </div>`;
};


let
    searchButton = $('.js-search-btn'),
    searchInput = $('.js-search-input'),
    resultBox = $('.js-result-box');

searchButton.on('click', () => {
  yaCounter39419275.reachGoal('SEARCH_BTN_CLICKED');

  const ID = searchInput.val();

  resultBox.empty();

  let results = data.filter((item) => item.id == ID );
  console.log(results[0]);

  if (results.length > 0) {
    resultBox.append(LabCardTemplate(1, results[0]));
  } else {
    resultBox.append(`<div>Не найдено</div>`)
  }
});