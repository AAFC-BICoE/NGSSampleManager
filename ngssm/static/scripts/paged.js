ko.observableArray.fn.paged = function (perPage, sortComparator) {
    var items = this;

    items.currentPage = ko.observable();
            items.pageSize = ko.observable(perPage);
            items.currentPageIndex = ko.observable(0);

            items.currentItemPage = ko.computed(function () {
                var pagesize = parseInt(items.pageSize(), 10),
                    startIndex = pagesize * items.currentPageIndex(),
                    endIndex = startIndex + pagesize;
                return this().slice(startIndex, endIndex);
            }, items);

            items.pagedItems = ko.computed(function () {
                var size = parseInt(items.pageSize(), 10),
                    start = items.currentPageIndex() * size;

                if (typeof (sortComparator) === "function") {
                    var sorted = this().sort(sortComparator);
                    return sorted.slice(start, start + size);
                } else {
                    return this().slice(start, start + size);
                }


            }, items);

            items.maxPageIndex = ko.computed(function () {
                return Math.ceil(this().length / items.pageSize()) - 1;
            }, items);

            items.allPages = ko.computed(function () {
                var pages = [];
                for (var i = 0; i <= items.maxPageIndex() ; i++) {
                    pages.push({ pageNumber: (i + 1) });
                }
                return pages;
            }, items);

            items.currentStatus = ko.computed(function () {
                var pagesize = parseInt(items.pageSize(), 10),
                    start = pagesize * items.currentPageIndex(),
                    end = start + pagesize;

                if (items.currentPageIndex() === items.maxPageIndex()) end = this().length;

                return 'Showing ' + (start + 1) + ' to ' + end + ' of ' + this().length;
            }, items);

            items.nextPage = function () {
                if (((items.currentPageIndex() + 1) * items.pageSize()) < items().length) {                 
                    items.currentPageIndex(items.currentPageIndex() + 1);
                } else {
                    items.currentPageIndex(0);
                }
            };

            items.previousPage = function () {
                if (items.currentPageIndex() > 0) {
                    items.currentPageIndex(items.currentPageIndex() - 1);
                } else {
                    items.currentPageIndex((Math.ceil(items().length / items.pageSize())) - 1);
                }
            };

            items.moveToPage = function (index) {
                items.currentPageIndex(index);
            };

            return items;
};
