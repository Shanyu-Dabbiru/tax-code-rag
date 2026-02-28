import React from 'react';
import { BookOpen } from 'lucide-react';
import SourceDocument, { SourceDocumentData } from './SourceDocument';

const DUMMY_SOURCES: SourceDocumentData[] = [
    {
        id: '1',
        section_number: '26 U.S.C. § 162',
        title: 'Trade or business expenses',
        text: '(a) In general\nThere shall be allowed as a deduction all the ordinary and necessary expenses paid or incurred during the taxable year in carrying on any trade or business, including—\n(1) a reasonable allowance for salaries or other compensation for personal services actually rendered;\n(2) traveling expenses (including amounts expended for meals and lodging other than amounts which are lavish or extravagant under the circumstances) while away from home in the pursuit of a trade or business...'
    },
    {
        id: '2',
        section_number: '26 U.S.C. § 212',
        title: 'Expenses for production of income',
        text: 'In the case of an individual, there shall be allowed as a deduction all the ordinary and necessary expenses paid or incurred during the taxable year—\n(1) for the production or collection of income;\n(2) for the management, conservation, or maintenance of property held for the production of income; or\n(3) in connection with the determination, collection, or refund of any tax.'
    }
];

export default function SourcesPane() {
    return (
        <div className="w-96 h-full bg-white border-l border-gray-200 flex flex-col shadow-sm">
            <div className="p-6 border-b border-gray-100 flex items-center gap-2">
                <BookOpen className="w-5 h-5 text-origin-accent" />
                <h2 className="text-lg font-semibold text-origin-text">Retrieved Tax Code</h2>
            </div>
            <div className="flex-1 p-6 overflow-y-auto">
                {DUMMY_SOURCES.map(doc => (
                    <SourceDocument key={doc.id} doc={doc} />
                ))}
            </div>
        </div>
    );
}
