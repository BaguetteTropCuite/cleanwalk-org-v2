import { format, add } from 'date-fns';
import { fr } from 'date-fns/locale';

const getCleanwalkWrittenDate = (startDate: Date, duration: number): string => {
  const endDate = add(startDate, { minutes: duration });

  const writtenDate = format(startDate, 'EEEE dd MMM yyyy', { locale: fr });
  const isSameYear = startDate.getFullYear() === new Date().getFullYear();

  const startDateString = format(startDate, isSameYear ? 'HH:mm' : 'dd MMM yyyy HH:mm');
  const endDateString = format(endDate, 'HH:mm');

  return `${writtenDate}${isSameYear ? '' : ` ${startDate.getFullYear()}`} de ${startDateString} à ${endDateString}`;
};

export default {
  getCleanwalkWrittenDate,
};
